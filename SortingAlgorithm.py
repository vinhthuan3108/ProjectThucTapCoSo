from main import InputData
class Sort(InputData):
    def __init__(self, data, key_index, order, rbTrucTiep, rbNhapTay, inputThanhPho, editNhietDo, editTocDoGio, editDoAm):
        super().__init__(rbTrucTiep, rbNhapTay, inputThanhPho, editNhietDo, editTocDoGio, editDoAm)
        self.data = data
        self.key_index = key_index
        self.order = order  
    def sort(self, algorithm="bubble"):
        if algorithm == "bubble":
            return self.bubble_sort()

        elif algorithm == "merge":
            return self.merge_sort()
        else:
            raise ValueError("Unsupported algorithm. Choose 'bubble' or 'merge'.")

    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.order == 'asc':
                    if self.data[j][self.key_index] > self.data[j + 1][self.key_index]:
                        self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                        swapped = True
                elif self.order == 'desc':
                    if self.data[j][self.key_index] < self.data[j + 1][self.key_index]:
                        self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                        swapped = True
            if not swapped:
                break
        return self.data

    def merge_sort(self):
        return self._merge_sort(self.data)
    def _merge_sort(self, data):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]
        left_sorted = self._merge_sort(left_half)
        right_sorted = self._merge_sort(right_half)
        return self._merge(left_sorted, right_sorted)
    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if self.order == 'asc':
                if left[i][self.key_index] < right[j][self.key_index]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            elif self.order == 'desc':
                if left[i][self.key_index] > right[j][self.key_index]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
        while i < len(left):
            result.append(left[i])
            i += 1
        while j < len(right):
            result.append(right[j])
            j += 1
        return result
