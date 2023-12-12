
# 1、日常操作
```sh
创建远程仓库
1、创建本地仓库
 git init design_pattern
 cd design_pattern
 touch a.txt
2、将文件上传暂存区
 git add .
3、传至本地仓库
 git commit -m ‘test’
4、github网站上创建远程仓库
5、将本地仓库和远程仓库进行关联
 git remote add design_pattern git@github.com:lindeci/design_pattern.git
6、将文件push到远程仓库
 git push -u design_pattern master
 
7、查看当前分支
 git branch 
8、查看本地和远程的所有分支
 git branch -a
9、删除远程分支
 git push design_pattern --delete master
10、删除本地的master分支
 git switch main
 git branch -D master
11、克隆指定分支
 git clone -b main git@github.com:lindeci/design_pattern.git
12、合并分支
 git merge ldc --allow-unrelated-histories
  --allow-unrelated-histories这句命令表示将ldc分支合并到当前分支，这里的两个本地分支各自追踪不同的远程库


1、init && clone
 git init 在当前目录新建一个仓库
 git init [project-name] 在一个目录下新建本地仓库
 git clone [url] 克隆一个远程仓库
2、diff
 git diff HEAD -- . 查看最新本地版本库和工作区所有文件的区别
 git diff HEAD -- [file-name] 查看最新本地版本库和工作区文件的却别
 git diff HEAD^ -- [file-name] 查看本地上一个版本和工作区文件的却别
 git diff [local branch] origin/[remote branch] 比较本地分支和远程分支的区别
3、status
 git status [file-name] 查看指定文件状态
 git status 查看所有文件状态
4、add
 git add [file-name1] [file-name2] ... 从工作区添加指定文件到暂存区
 git add . 将工作区的被修改的文件和新增的文件提交到暂存区，不包括被删除的文件
 git add -u . u指update，将工作区的被修改的文件和被删除的文件提交到暂存区，不包括新增的文件
 git add -A . A指all，将工作区被修改、被删除、新增的文件都提交到暂存区
5、commit
 git commit -m [massage] 将暂存区所有文件添加到本地仓库
 git commit [file-name-1] [file-name-2] -m [massage] 将暂存区指定文件添加到本地仓库
 git commit -am [massage] 将工作区的内容直接加入本地仓库
 git commit --amend 快速将当前文件修改合并到最新的commit，不会产生新的commit。在提交commit后发现还有部分文件修改忘记提交了可以是用该命令
   加-m是指直接在后面写上版本的注释，不加-m的话会用一个vim打开文件让你写入massage，有未追踪的文件将会失败，需要add加入暂存区。
6、clean
 git clean -df 加-d是指包含目录，加-f是指强制，删除所有未跟踪的文件
7、log
 git log 显示所有commit日志
 git log --pretty=oneline 将日志缩写为单行显示
 git log --graph --pretty=oneline --abbrev-commit 查看分支合并情况
 git log --oneline --decorate --graph --all 查看分叉历史，包括：提交历史、各个分支的指向以及项目的分支分叉情况。
 git log -3 查看最新3条commit日志数据
8、reflog
 git reflog 显示操作本地版本库的命令，包括commit和reset等，在回退版本以后又后悔找不到commit id了可以使用此命令查看历史
9、push
 git push 将文件添加到远程仓库
 git push -f 强制提交，当我们本地reset到旧的版本时，然后普通push会被拦截，因为此是本地HEAD指向比远程库还要旧
 git push origin [branch-name] 推送当前本地分支到指定远程分支
10、rm
 git rm --cached [file-name] 删除暂存区的文件
 git rm -rf . 不但删除所有暂存区的文件，还删除所有工作区的物理文件
11、checkout
 git checkout -- [file-name]
   最好加--，没有的话就把它当作切换分支看待，切换到另一个分支了，如果没有这个分支也会把它当作文件执行。
   用暂存区的文件覆盖掉工作区的文件
   如果暂存区没有可更新的就会用commit的文件更新工作区的文件
 git checkout [branch] 切换分支
 git checkout -b [new-branch-name] 创建并切换分支
12、reset
 对整个版本进行操作
 git reset --{soft|(mixed)|hard} HEAD
  --soft 其中可选参数soft表示单纯的切换HEAD指向的commit-id
  --mixed 默认值mixed参数表示先执行上面一步，然后再将commit-id里面的内容更新到暂存区
  --hard hard表示先执行上面两步，然后再将暂存区内容同步到工作区
 git reset --hard HEAD^^ 用上两个版本里的所有文件撤回到暂工作区
 git reset --hard [commit id] 用指定版本的所有文件撤回到工作区
 对当个文件进行操作
 git reset HEAD [file-name]
  对单个文件操作时候只能用mixed参数，而且还是可省略
  对单个文件操作时候HEAD指向不会变
  将commit中指定的文件同步到暂存区中
 git reset [commit-id] [file-name] 将指定commit-id中的文件替换掉暂存区的文件
13、revert
 撤回版本的比较
 git revert -n [commit-id]
 git revert -n HEAD^^
14、branch
 git branch [branch-name] 创建分支
 git branch 查看当前分支
 git branch -a 查看本地和远程的所有分支
 git branch -r 查看远程所有分支
 git branch -d [branch-name] 删除一个分支
 git branch -D [branch-name] 强制删除一个没有合并的分支
 git branch --set-upstream-to=origin/[branch-name] [branch-name] 把本地分支和远程分支进行连接
15、merge
 git merge 合并本地origin/[branch-name]和HEAD->[branch-name]的代码，并同步到工作空间
 git merge [branch-name] 用于合并指定分支到当前分支
 git merge --quit 退出当前分支合并，当合并后冲突很多，要撤回合并分支就可以用这个命令
 git merge --no-ff -m [massage] [branch-name] 不使用Fast forward合并分支，这样会创建新的commit，所以需要massage。这样被合并的分支HEAD指向是会变的。
  如果使用了Fast forward方式合并分支，那么删除次要分支的时候历史分支记录也会被删除，这样就无法追寻分支合拼信息了。
16、switch
 git switch -c [branch-name] 创建新分支并切换到该分支
 git switch [branch-name] 切换到已有分支
19、remote
 git remote add origin 远程地址 关联远程仓库
 git remote 查看本地添加了哪些远程分支地址
 git remote -v 查看本地添加了哪些远程分支地址更详细信息
 git remote remove origin 删除本地指定的远程地址
20、fetch
 git fetch 拉取远程分支最新的commit到本地仓库的origin/[branch-name]
21、pull
 git pull 从远程仓库拉取代码到工作空间
24、rebase
 git rebase -i HEAD~2 
 合并前两个历史提交，会弹出vim修改信息，修改第二行的pick为s，或者为squash，squash为合并的意识，然后保存退出编辑，
 会打开第二个vim编辑，合并并修改commit内容，保存退出会产生一个新的commit id，这样就合并了两个commit
 
25、git clone 指定分支
 git clone -b 分支名称 git地址

26、设置代理
 git config --global http.proxy 'socks5://10.206.32.13:7890' 
 git config --global https.proxy 'socks5://10.206.32.13:7890'
 取消代理：
 git config --global --unset http.proxy
 git config --global --unset https.proxy
 查看配置信息：
 git config -l --global

27、linux设置git用户名和密码
 进入项目目录
 命令:git config --global credential.helper store
```

# 28、linux设置账号密码
```
git config --global user.name lindeci
git config --global user.password
git config --global user.email 541287039@qq.com

my class token: 
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
```

# 29、上传大文件
```
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
apt-get install git-lfs
git lfs install

git lfs --version

git lfs ls-files   # 这个命令会列出所有被Git LFS跟踪的文件

# 添加跟踪文件
git lfs track "*.tar.gz"
git add .gitattributes
git commit -m "Track .tar.gz files with Git LFS"

# 将大文件添加到了Git仓库中
git add mysql-debug-docker.tar.gz
git commit -m "Add large file"

# 上传
git push mysql-server-8.2.0-docker main
```

# 30、不小心提交敏感信息的处理

1. 创建一个孤立分支，并切换到该分支：
```bash
git checkout --orphan latest_branch
```
2. 暂存所有文件：
```bash
git add -A
```
3. 提交所有更改：
```bash
git commit -am "First Commit"
```
4. 删除主分支 main
```bash
git branch -D main
```
5. 重命名当前分支为 main
```bash
git branch -m main
```
6. 强制推送本地分支：
```bash
git push -f origin main
```