# home-assistant-stable-tag
A stable docker tag which always point to the penultimate home assistant release. Usefull if you auto-update your docker images with [watchtower](https://github.com/containrrr/watchtower).


# How to use?

Replace your Home Assistant docker tag by the following: `skaronator/home-assistant-stable-tag:latest`

The `latest` tag will be updated just like the original home-assistant docker tag but instead of pointing to the latest version it will point to a penultimate home assistant release.

| homeassistant/home-assistant:latest Version | skaronator/home-assistant-stable-tag:latest Version |
|---------------------------------------------|-----------------------------------------------------|
| 0.110.0                                     | 0.109.6                                             |
| 0.110.1.. 2.. 3..                           | 0.109.6                                             |
| 0.110.7 (last patch for 0.110)              | 0.109.6                                             |
| 0.111.0 (new release)                       | 0.110.7 (Upgrading to penultimate Version)          |
| 0.111.1.. 2.. 3..                           | 0.110.7                                             |

# When does it work?

The Github CI will run the little python script on scheduled base. The script loads all the available home assistant tags from the docker registry. After that it'll figure out what the penultimate stable release was and pull it and push it to my docker repository.

# Why?

I update all my docker containers with [watchtower](https://github.com/containrrr/watchtower) on a daily baises. This works great for all containers and I'm using it now for well over 2 years but home assistant sometimes cause trouble. If you upgrade Home Assistant manually you could just wait 2-3 days before upgrading and everything will work fine.

Why does Home Assistant doesn't provide a similar stable tag? I can only guess here but I understand why they don't want to provide it. They are still at 0.xx verions with a lot of (breaking) changes between each release and they want to have as many people testing thier new releases as possible. When everyone just stay at the stable tag we'd just have the same situration and I'd probably create a stable-stable tag.
