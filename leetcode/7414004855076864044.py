def solution(N, M, data):
    visit_list = [[False for _ in range(M)] for _ in range(N)]

    special_part = [(0, -1, 'R'), (0, 1, 'L'), (1, 0, 'U'), (-1, 0, 'D')]

    common_part = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    start_point = None
    for i in range(N):
        for j in range(M):
            if data[i][j] == 'O':
                start_point = (i, j)
                break
        if start_point:
            break

    from collections import deque

    q = deque()

    q.append(start_point)

    while q:

        x, y = q.popleft()

        for dx, dy, target_special in special_part:
            i = x + dx
            j = y + dy

            if 0 <= i < N and 0 <= j < M:

                if data[i][j] == target_special and not visit_list[i][j]:

                    visit_list[i][j] = True
                    q.append((i,j))

        for dx, dy in common_part:
            i = x + dx
            j = y + dy

            if 0 <= i < N and 0 <= j < M:

                if data[i][j] == '.' and not visit_list[i][j]:
                    visit_list[i][j] = True
                    q.append((i, j))

    count_no = 0
    for i in range(N):
        for j in range(M):
            if data[i][j] != 'O' and not visit_list[i][j]:
                count_no += 1

    for x in range(N):
        print(visit_list[x])

    return count_no


if __name__ == "__main__":
    # Add your test cases here
    pattern = [
        [".", ".", ".", ".", "."],
        [".", "R", "R", "D", "."],
        [".", "U", ".", "D", "R"],
        [".", "U", "L", "L", "."],
        [".", ".", ".", ".", "O"]
    ]
    print(solution(5, 5, pattern) == 10)
