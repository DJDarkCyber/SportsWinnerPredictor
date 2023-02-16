from bs4 import BeautifulSoup
import requests

def getUserProfile(user_name):
    r = requests.get("https://github.com/" + user_name)
    
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')

    full_name =  soup.find(class_='vcard-fullname')
    full_name = full_name.get_text().lstrip().rstrip()

    usr_desc = soup.find(class_="user-profile-bio")
    usr_desc = usr_desc.get_text().lstrip().rstrip()

    usr_img = soup.find(class_="avatar-user")
    usr_img = usr_img.get("src")

    pinned_cont = soup.find_all(class_="js-pinned-items-reorder-container")
    # print(pinned_cont)

    pinned_repositories = []
    pinned_repo_links = []
    pinned_repo_desc = []

    for stuff in pinned_cont:
        repos = stuff.find_all(class_="repo")
        for repo in repos:
            repo = repo.get_text()
            pinned_repositories.append(repo)
            pinned_repo_links.append("https://github.com/" + user_name + "/" + repo)
        
        repo_descs = stuff.find_all(class_="pinned-item-desc")
        for repo_desc in repo_descs:
            repo_desc = repo_desc.get_text()
            repo_desc = repo_desc.replace("\n", "")
            repo_desc = repo_desc.lstrip().rstrip()
            pinned_repo_desc.append(repo_desc)
    
    print(full_name)
    print(usr_desc)
    print(usr_img)
    print(pinned_repo_desc)

    return full_name, usr_desc, usr_img, pinned_repositories, pinned_repo_links, pinned_repo_desc


def getUsrRepo(user_name, repo_name):
    r = requests.get("https://github.com/" + user_name + "/" + repo_name)
    content = r.content
    soup = BeautifulSoup(content, "html.parser")

    repo_stars = soup.find(id="repo-stars-counter-star")
    repo_stars = repo_stars.get_text()

    repo_forks = soup.find(id="repo-network-counter")
    repo_forks = repo_forks.get_text()

    repo_about = soup.find(class_="my-3")
    repo_about = repo_about.get_text().lstrip().rstrip()

    return repo_stars, repo_forks, repo_about

getUsrRepo("DJDarkCyber", "SportsWinnerPredictor")