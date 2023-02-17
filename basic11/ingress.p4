
/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

#include "telemet.p4"

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

            //process_int.apply(hdr, metadata);


            if (hdr.ipv4.src_addr == 0x0a000101 || hdr.ipv4.dst_addr == 0x0a000101) {
            standard_metadata.priority = (bit<3>)7;
            ipv4_lpm.apply();

            }

            else if (hdr.ipv4.src_addr == 0x0a000202 || hdr.ipv4.dst_addr == 0x0a000202){
            standard_metadata.priority = (bit<3>)0;
            ipv4_lpm.apply();

        }

        }
    }
}
