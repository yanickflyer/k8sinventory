import minimal, argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Kubernetes Inventory Report", add_help=True)
    parser.add_argument('--minimal', '-m', help='Generate minimal report', action='store_true')
    parser.add_argument('--csv', dest='csv_filepath',help='Set filepath export report to CSV. If FilePatch not specified it uses current directory', metavar='PATH')
    args = parser.parse_args()


    # parser.add_argument('--
    # Check if user specified --out csv
    # if "--full" in sys.argv:
    #     final_report = generate_inventory.get_report(minimal=False)
    #     cluster_name = final_report['cluster_name'] if final_report else 'default_cluster_name'
    #     print(json.dumps(final_report))
    #     export_csv(final_report, cluster_name, minimal=False)
    if args.minimal:
        print("Generating minimal report...")
        filepath = args.csv_filepath if args.csv_filepath else None
        minimal.get_report(filepath)

if __name__ == "__main__":
    main()