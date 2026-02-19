# Commit 흐름

git switch main
git pull origin main         // 1️⃣ main 최신화

git switch -c branch       // 2️⃣ 브랜치 생성

**(작업)**

git add . 
git commit -m "feat: 기능"  // 3️⃣ 커밋

git push -u origin branch  // 4️⃣ 브랜치 push

git switch main
git pull origin main          // 5️⃣ 다시 최신화

git merge branch          // 6️⃣ 병합

git push origin main          // 7️⃣ 최종 push
