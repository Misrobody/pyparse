from termcolor import colored

class Stats:
    def __init__(self):
        pass
    
    def print_call_stats(self, call_resolver):
        stats = call_resolver.stats()
        
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

        print("\nOut-App Callees breakdown:")
        print(colored(f"{'Modules:':<20}{stats['modules']:>10} ({_rate('modules')})", "yellow"))
        print(colored(f"{'Methods:':<20}{stats['methods']:>10} ({_rate('methods')})", "blue"))

        print("=" * 40)
        
    def print_dataflow_stats(self, dataflow_resolver):
        stats = dataflow_resolver.stats()
        
        print("=" * 40)
        print(colored("Statistics Overview", "cyan", attrs=["bold"]))
        print("=" * 40)

        

        