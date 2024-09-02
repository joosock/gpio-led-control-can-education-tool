import argparse
import threading
import IPC_Library
import time

def sendtoCAN(channel, canId, sndDataHex):
        sndData = parse_hex_data(sndDataHex)
        uiLength = len(sndData)
        ret = IPC_SendPacketWithIPCHeader("/dev/tcc_ipc_micom", channel, IPC_Library.TCC_IPC_CMD_CA72_EDUCATION_CAN_DEMO, IPC_IPC_CMD_CA72_EDUCATION_CAN_DEMO_START, canId, sndData, uiLength)

def receiveFromCAN():
        micom_thread = threading.Thread(target=IPC_Library.IPC_ReceivePacketFromIPCHeader, args=("/dev/tcc_ipc_micom", 1))
        micom_thread.start()

def main():
    parser = argparse.ArgumentParser(description="IPC Sender/Receiver")
    parser.add_argument("mode", choices=["snd", "rev"], help="Specify 'snd' to send a packet or 'rev' to receive a packet.")
    parser.add_argument("--file_path", default="/dev/tcc_ipc_micom", help="File path for IPC communication")
    parser.add_argument("--channel", type=int, default=0, help="Specify the IPC channel.")
    parser.add_argument("--uiCmd1", type=int, default=IPC_Library.TCC_IPC_CMD_CA72_EDUCATION_CAN_DEMO, help="Value for uiCmd1")
    parser.add_argument("--uiCmd2", type=int, default=IPC_Library.IPC_IPC_CMD_CA72_EDUCATION_CAN_DEMO_START, help="Value for uiCmd2")
    parser.add_argument("--uiCmd3", type=int, default=1, help="Value for uiCmd3")
    parser.add_argument("--sndDataHex", type=str, help="Value for sndData as a hex string, e.g., '12345678'")
    parser.add_argument("--sndDataStr", type=str, help="Value for sndData as a string, e.g., 'Hello!!!'")
    parser.add_argument("--defaultHex", type=str, default="12345678", help="Default hex data if no sndDataHex provided")

    args = parser.parse_args()
    print(f"args.mode {args.mode} args.file_path {args.file_path} args.channel {args.channel}")

    if args.mode == "snd":
        if args.uiCmd1 is None or args.uiCmd2 is None:
            print("Please provide values for uiCmd1 and uiCmd2.")
            return

        uiCmd1 = args.uiCmd1
        uiCmd2 = args.uiCmd2
        uiCmd3 = args.uiCmd3

        if args.sndDataHex:
            sndData = IPC_Library.parse_hex_data(args.sndDataHex)
        elif args.sndDataStr:
            sndData = IPC_Library.parse_string_data(args.sndDataStr)
        else:
            # Use defaultHex if no data provided
            sndData = IPC_Library.parse_hex_data(args.defaultHex)

        uiLength = len(sndData)

        print(f"file_path: {args.file_path}")
        print(f"channel: {args.channel}")
        print(f"uiCmd1: {uiCmd1}")
        print(f"uiCmd2: {uiCmd2}")
        print(f"uiCmd3: {uiCmd3}") 
        print(f"sndData: {sndData}")
        print(f"uiLength: {uiLength}")

        ret = IPC_Library.IPC_SendPacketWithIPCHeader(args.file_path, args.channel, uiCmd1, uiCmd2, uiCmd3, sndData, uiLength)


    elif args.mode == "rev":
        micom_thread = threading.Thread(target=IPC_Library.IPC_ReceivePacketFromIPCHeader, args=("/dev/tcc_ipc_micom", 1))
        micom_thread.start()

        ca53_thread = threading.Thread(target=IPC_Library.IPC_ReceivePacketFromIPCHeader, args=("/dev/tcc_ipc_ap", 1))
        ca53_thread.start()

        # From IPC_Library
        while True:
            print("IPC_Library.received_pucData", ' '.join(format(byte, '02X') for byte in IPC_Library.received_pucData))
            time.sleep(1)

    else:
        print("Invalid mode. Use 'snd' or 'rev'.")
        return

if __name__ == "__main__":
    main()

#python3 main.py rev
#python3 main.py snd        
          