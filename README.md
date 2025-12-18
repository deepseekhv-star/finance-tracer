Các topic đã thực hiện trong project:
1. Topic 1: Budget Management System — 6 points
    - Hiển thị:
        o	Total budget
        o	Total spent
        o	Remaining budget
        o	Over budget warning
    - Khi tạo transaction → phải cộng dồn và theo dõi số tiền đã chi
    - Sync với transaction (khi tạo/sửa/xóa)
    - Dashboard theo tháng/năm

2. Topic 2: Orphaned Transactions (Category Delete) — 3 points
    - Tạo 1 category(Expence/Income) = “Uncategorized”
    - Khi xóa category → các transaction liên quan chuyển category = “Uncategorized”  

3. Topic 3: Category Update + Transaction Sync — 3 points
    - Khi update category → update toàn bộ transaction có category_name đó
    - Khi update category → update budget có category_name đó

4. Topic 4: Budget Integrity (Category Delete) — 2 points   
    - Khi xóa Category -> Budget của category đó cũng phải xóa