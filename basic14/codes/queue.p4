/*************************************************************************
************   Adding INT to the Packet  *************
*************************************************************************/

control process_queue (
    inout headers hdr,
    inout local_metadata_t metadata,
    inout standard_metadata_t standard_metadata) {

    /*Queue with index 0 is the bottom one, with lowest priority*/
    register<bit<32>>(8) queue_bound;

    action queue_a(){



    }


table queue_t {

  actions = {
        queue_a;
        NoAction;
    }
    const default_action = NoAction();
}

apply {
    queue_t.apply();

}

}
