class Note:
    def __init__(self, left, data, right):
        self.left = left
        self.data = data
        self.right = right



class LinkNote:
    def __init__(self):
        self.head = None

    def append(self, data):
        if self.head:
            last_note = self.head
            while True:

                if last_note.right is not None:
                    last_note = last_note.right
                else:
                    break

            note = Note(last_note, data, None)
            last_note.right = note

        else:
            self.head = Note(None, data, None)

    def get_list(self):

        return_list = []
        last_note = self.head
        while True:
            if last_note.right is not None:
                return_list.append(last_note.data)
                last_note = last_note.right
            else:
                return_list.append(last_note.data)
                break

        return return_list


    def check_item(self, data):
        last_note = self.head
        mark_true = False
        while True:
            if last_note.right is not None:
                if last_note.data == data:
                    mark_true = True
                    break
                last_note = last_note.right
            else:
                if last_note.data == data:
                    mark_true = True
                return mark_true

        
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    point_val = arr[len(arr) // 2]
    left = [x for x in arr if x < point_val]
    right = [x for x in arr if x > point_val]
    middle = [x for x in arr if x == point_val]

    return quick_sort(left) + middle + quick_sort(right)


def build_pmt(pattern):
    pmt = [0 for _ in pattern]
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = pmt[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pmt[i] = j
        else:
            pmt[i] = 0
    return pmt

def kmp_alg(ori_string, pattern):

    pmt = build_pmt(pattern)
    j = 0
    m = len(pattern)
    count_p = 0
    for i in range(0, len(ori_string)):
        while j > 0 and ori_string[i] != pattern[j]:
            j = pmt[j - 1]
        if ori_string[i] == pattern[j]:
            j += 1

        if j == m:
            count_p += 1

            j = pmt[j - 1]

    return count_p


print(kmp_alg("xyxyxyx", "xyx"))


