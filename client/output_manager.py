class OutputManager:

    def print_file_version(self):
        print("TP-PING v0.1")

    # only one of the options must be true
    def print_operation(self, is_ping, is_reverse, is_proxy):
        op_name = ""
        if is_ping:
            op_name = "Direct Ping"
        elif is_reverse:
            op_name = "Reverse Ping"
        elif is_proxy:
            op_name = "Proxy Ping"
        else:
            op_name = "Unknown"
        print(f"Operation: {op_name}")

    def print_server(self, addr):
        print(f"Server Address: {addr}")

    def print_client(self, addr):
        print(f"Client Address: {addr}")

    def print_latest_message(self, n_bytes, from_addr, n_seq, time_ms):
        rounded_time = round(time_ms, 1)
        sent_str = f"{n_bytes} bytes from {from_addr}"
        print(f"{sent_str}: seq={n_seq} time={rounded_time} ms")

    def print_statistics(self, addr, n_packs, n_packs_rcvd, time_ms, rtt_list):
        # packets satistics
        packs_lost = n_packs - n_packs_rcvd
        packs_lost_percentage = round(packs_lost * 100 / n_packs)
        inf_transm = f"{n_packs} packets transmitted"
        inf_recvd = f"{n_packs_rcvd} received"
        inf_lost = f"{packs_lost_percentage} % packet loss"
        inf_time = f"time {time_ms}ms"

        # rtt statistics
        rtt_start = "rtt min/avg/max/mdev"
        rtt_min = "{:.3f}".format(min(rtt_list))
        rtt_max = "{:.3f}".format(max(rtt_list))
        rtt_avg = "{:.3f}".format(sum(rtt_list) / len(rtt_list))
        rtt_mdev = "{:.3f}".format(0)   # todo: buscar formula

        print(f"\n--- {addr} ping statistics ---")
        print(f"{inf_transm}, {inf_recvd}, {inf_lost}, {inf_time}")
        print(f"{rtt_start} = {rtt_min}/{rtt_avg}/{rtt_max}/{rtt_mdev} ms")
