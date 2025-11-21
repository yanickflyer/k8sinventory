import workload, argparse, fullworkload

def main():
    parser = argparse.ArgumentParser(description="Generate Kubernetes Inventory Report", add_help=True)
    parser.add_argument('--workload', '-w', help='Generate Workload report', action='store_true')
    parser.add_argument('--full', '-f', help='Generate Full Workload report', action='store_true')
    parser.add_argument('--csv', dest='csv_filepath',help='Set filepath export report to CSV. If FilePath not specified it uses current directory', metavar='PATH')
    args = parser.parse_args()


    # parser.add_argument('--
    # Check if user specified --out csv
    # if "--full" in sys.argv:
    #     final_report = generate_inventory.get_report(minimal=False)
    #     cluster_name = final_report['cluster_name'] if final_report else 'default_cluster_name'
    #     print(json.dumps(final_report))
    #     export_csv(final_report, cluster_name, minimal=False)
    if args.workload:
        print("Generating Workload report...")
        filepath = args.csv_filepath if args.csv_filepath else None
        workload.get_report(filepath)
    elif args.full:
        print("Generating Full Workload report...")
        filepath = args.csv_filepath if args.csv_filepath else None
        final_report = fullworkload.get_report(filepath)
        print(final_report)
        # export_csv(final_report, cluster_name, minimal=False)

if __name__ == "__main__":
    main()