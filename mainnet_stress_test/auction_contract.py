from pyteal import *

def approval_program():
    highest_bidder = Bytes("highest_bidder")
    highest_bid = Bytes("highest_bid")

    on_creation = Seq([
        App.globalPut(highest_bidder, Global.creator_address()),
        App.globalPut(highest_bid, Int(0)),
        App.globalPut(Bytes("auction_end"), Global.latest_timestamp() + Int(86400)),
        Return(Int(1))
    ])

    on_call = Seq([
        # Ensure there is a payment transaction accompanying the app call
        Assert(Global.group_size() == Int(2)),
        Assert(Gtxn[0].type_enum() == TxnType.Payment),
        Assert(Gtxn[1].type_enum() == TxnType.ApplicationCall),
        Assert(Gtxn[1].application_id() == Global.current_application_id()),
        
        # Compliance Checks (Reviewer Requirements)
        Assert(Global.latest_timestamp() <= App.globalGet(Bytes("auction_end"))),
        Assert(App.optedIn(Gtxn[0].sender(), Global.current_application_id())),
        
        # Payment must be directed to the app address
        Assert(Gtxn[0].receiver() == Global.current_application_address()),

        # Bid must be greater than current highest bid
        Assert(Gtxn[0].amount() > App.globalGet(highest_bid)),

        # Refund previous bidder (if first bid, refunds 0 to creator)
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: App.globalGet(highest_bidder),
            TxnField.amount: App.globalGet(highest_bid),
            TxnField.fee: Int(0) # Requires fee pooling from outer transaction
        }),
        InnerTxnBuilder.Submit(),

        # Update global state
        App.globalPut(highest_bidder, Gtxn[0].sender()),
        App.globalPut(highest_bid, Gtxn[0].amount()),

        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.NoOp, on_call],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(0))],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Int(0))],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(0))]
    )
    return program

def clear_state_program():
    return Return(Int(1))
