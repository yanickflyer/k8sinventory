import workload, argparse, fullworkload

def main():
    parser = argparse.ArgumentParser(description="Generate Kubernetes Inventory Report", add_help=True)
    parser.add_argument('--workload', '-w', help='Generate Workload report', action='store_true')
    parser.add_argument('--full', '-f', help='Generate Full Workload report', action='store_true')
    parser.add_argument('--csv', dest='csv_filepath',help='Set filepath export report to CSV. If FilePath not specified it uses current directory', metavar='PATH')
    args = parser.parse_args()

    if args.workload:
        print("Generating Workload report...")
        filepath = args.csv_filepath if args.csv_filepath else None
        workload.get_report(filepath)
    elif args.full:
        print("Generating Full Workload report...")
        filepath = args.csv_filepath if args.csv_filepath else None
        fullworkload.get_report(filepath)

if __name__ == "__main__":
    main()