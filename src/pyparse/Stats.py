from termcolor import colored

class Stats:     
    def print_call_stats(self, call_resolver):
        stats = call_resolver.get_stats()
        stats["total_resolved"] = stats["callees"] + stats["modules"] + stats["methods"]
        stats["total_unresolved"] = stats["total"] - stats["total_resolved"]
        stats["out-app"] = stats["modules"] + stats["methods"]
        
        def _rate(key):
            return f"{(stats[key] / stats['total'] * 100):.2f}%"

        print("=" * 40)
        print(colored("Statistics Overview", "cyan", attrs=["bold"]))
        print("=" * 40)
        
        print(f"{'Total:':<20}{stats['total']:>10}")
        print(f"{'Resolved:':<20}{stats['total_resolved']:>10} ({_rate('total_resolved')})")
        print(colored(f"{'Unresolved:':<20}{stats['total_unresolved']:>10} ({_rate('total_unresolved')})", "red"))

        print("\nCall Categories:")
        print(f"{'In-app callees:':<20}{stats['callees']:>10} ({_rate('callees')})")
        print(f"{'Out-app callees:':<20}{stats['out-app']:>10} ({_rate('out-app')})")

        print("\nOut-App Callees breakdown:")
        print(colored(f"{'Modules:':<20}{stats['modules']:>10} ({_rate('modules')})", "yellow"))
        print(colored(f"{'Methods:':<20}{stats['methods']:>10} ({_rate('methods')})", "blue"))

        print("=" * 40)
        
    def print_dataflow_stats(self, dataflow_resolver):
        stats = dataflow_resolver.get_stats()
        stats["total_resolved"] = stats["func"] + stats["calls"]
        stats["total_unresolved"] = stats["total"] - stats["total_resolved"]
        stats["in-app"] = stats["func"] + stats["calls"]
        stats["out-app"] = 0
 
        def _rate(key):
            return f"{(stats[key] / stats['total'] * 100):.2f}%" 
        
        print("=" * 40)
        print(colored("Statistics Overview", "cyan", attrs=["bold"]))
        print("=" * 40)
        
        print(f"{'Total:':<20}{stats['total']:>10}")
        print(f"{'Resolved:':<20}{stats['total_resolved']:>10} ({_rate('total_resolved')})")
        print(colored(f"{'Unresolved:':<20}{stats['total_unresolved']:>10} ({_rate('total_unresolved')})", "red"))
        
        print("\nCall Categories:")
        print(f"{'In-app callees:':<20}{stats['in-app']:>10} ({_rate('in-app')})")
        print(f"{'Out-app callees:':<20}{stats['out-app']:>10} ({_rate('out-app')})")
        
        print("\nIn-App Callees breakdown:")
        print(f"{'Operations:':<20}{stats['func']:>10} ({_rate('func')})")
        print(f"{'Datacalls:':<20}{stats['calls']:>10} ({_rate('calls')})")        
        
        print("=" * 40)


        

        