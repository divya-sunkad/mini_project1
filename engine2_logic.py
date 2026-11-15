import math

class StudentNode:
    """Represents a student attendance calculation node."""
    def __init__(self, usn, name, held, attended):
        self.usn = usn
        self.name = name
        self.held = held
        self.attended = attended
        self.pct = 0.0 if held <= 0 else round((attended / held) * 100.0, 2)
        # FR-09 Recovery Target: ceil((0.75 * held - attended) / 0.25)
        self.recovery = max(0, math.ceil(((0.75 * held) - attended) / 0.25))
        self.status = "Safe" if self.pct >= 75.0 else ("Warning" if self.pct >= 65.0 else "Detention")

    def __lt__(self, other):
        # Min-Heap ordering: lowest percentage gets highest priority
        return self.pct < other.pct

class AttendanceMinHeap:
    """Hand-built Min-Heap Priority Queue built from scratch using array."""
    def __init__(self):
        self.heap = []

    def push(self, node: StudentNode):
        self.heap.append(node)
        self._sift_up(len(self.heap) - 1)

    def pop_min(self) -> StudentNode:
        if not self.heap: raise IndexError("Heap is empty")
        min_node = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return min_node

    def peek(self) -> StudentNode:
        return self.heap[0] if self.heap else None

    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        smallest = idx
        left, right = 2 * idx + 1, 2 * idx + 2
        n = len(self.heap)
        if left < n and self.heap[left] < self.heap[smallest]: smallest = left
        if right < n and self.heap[right] < self.heap[smallest]: smallest = right
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._sift_down(smallest)

def run_engine2_demo():
    print("=" * 75)
    print(" ENGINE 2: LOGIC & RULE (HAND-BUILT MIN-HEAP SHORTAGE QUEUE)")
    print("=" * 75)
    students_data = [
        ("01FE24BCA274", "Soumya Sunkad", 10, 10), # 100.0% -> Safe
        ("01FE24BCA275", "Divya Sunkad",  10, 7),  # 70.0%  -> Warning
        ("01FE24BCA276", "Akkamma S R",   10, 8),  # 80.0%  -> Safe
        ("01FE24BCA277", "Rahul Patil",   10, 5),  # 50.0%  -> Detention
    ]
    min_heap = AttendanceMinHeap()
    for usn, name, held, att in students_data:
        min_heap.push(StudentNode(usn, name, held, att))

    print(f"[*] Peek Most Critical Student in O(1): {min_heap.peek().name} ({min_heap.peek().pct}%)\n")
    print(f"{'Priority':<10} | {'USN':<14} | {'Name':<16} | {'%':<8} | {'Status':<12} | {'Recovery Target'}")
    print("-" * 75)
    rank = 1
    while min_heap.heap:
        st = min_heap.pop_min()
        rec_text = f"{st.recovery} consecutive classes" if st.recovery > 0 else "None (Safe)"
        print(f"#{rank:<9} | {st.usn:<14} | {st.name:<16} | {st.pct:<7}% | {st.status:<12} | {rec_text}")
        rank += 1

if __name__ == "__main__":
    run_engine2_demo()