class DisplayWindow:
    def __init__(self, root):
        self.root = root

    def update_metrics(self, elapsed_time, total_time, memory_usage):
        # Dummy implementation for updating display metrics
        print(f"Elapsed Time: {elapsed_time:.2f}s, Total Time: {total_time:.2f}s, Memory Usage: {memory_usage:.2f} MB")
