
/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

#include "telemet.p4"
#include "classification.p4"

control MyIngress(inout headers hdr,
                  inout local_metadata_t metadata,
                  inout standard_metadata_t standard_metadata) {

    /*Queue with index 0 is the bottom one, with lowest priority*/
    register<bit<32>>(8) queue_bound;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(macAddr_t dst_addr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.src_addr = hdr.ethernet.dst_addr;
        hdr.ethernet.dst_addr = dst_addr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dst_addr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }



    apply {
        if (hdr.ipv4.isValid()) {

            if(hdr.ipv4.protocol ==6) {

            process_int.apply(hdr, metadata);
            classification.apply(hdr, metadata, standard_metadata);

            }
        }
    }
}
