bold=$(tput bold)
normal=$(tput sgr0)
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

git checkout dev
git push
git checkout production
git pull origin dev
git push
git checkout dev

echo -e "\n✅ ${green}Operation finished${reset}"