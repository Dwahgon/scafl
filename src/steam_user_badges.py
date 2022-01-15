import bs4
import requests
import re


class SteamUserBadges:
    def __init__(self, cookies) -> None:
        self.cookies = cookies
        self.profile_url = (
            f'https://steamcommunity.com/profiles/{cookies["steamLoginSecure"][:17]}'
        )

    def get_badges(self):
        current_badge_page = 1
        page_count = 1
        badges = []
        while current_badge_page <= page_count:
            badge_page = self.get_badge_page(current_badge_page)

            if current_badge_page == 1:
                page_count = self.get_badge_page_count(badge_page)

            for badge_node in badge_page.find_all(
                "div", {"class": "badge_row is_link"}
            ):
                badge_data = self._new_badge_dict(
                    badge_id=self.get_badge_node_game_id(badge_node),
                    badge_name=self.get_badge_node_game_name(badge_node),
                    badge_drop_count=self.get_badge_node_drop_count(badge_node),
                )
                if badge_data["id"] != "0":
                    badges.append(badge_data)
            current_badge_page += 1
        return badges

    def get_badges_with_remaining_drops(self):
        return [badge for badge in self.get_badges() if badge["drop_count"] > 0]

    def get_badge_page_count(self, badge_page):
        badge_page_count_node = badge_page.find_all("a", {"class": "pagelink"})
        if len(badge_page_count_node) == 0:
            return 1
        return int(badge_page_count_node[-1].text)

    def get_badge_page(self, page_number):
        request = requests.get(
            f"{self.profile_url}/badges/?p={page_number}", cookies=self.cookies
        )
        return bs4.BeautifulSoup(request.text, "html.parser")

    def get_badge_data(self, badge_id):
        request = requests.get(
            self.profile_url + "/gamecards/" + badge_id + "/", cookies=self.cookies
        )
        badge_data = bs4.BeautifulSoup(request.text, "html.parser")
        return self._new_badge_dict(
            badge_id=badge_id,
            badge_name=self.get_badge_node_game_name(badge_data),
            badge_drop_count=self.get_badge_node_drop_count(badge_data),
        )

    def get_badge_node_drop_count(self, badge_node):
        drop_count = 0
        drop_count_node = badge_node.find("span", {"class": "progress_info_bold"})
        if drop_count_node is not None:
            drop_count_text = drop_count_node.contents[0]
            drop_count = (
                0
                if "No card drops" in drop_count_text
                else int(drop_count_text.split(" ", 1)[0])
            )
        return drop_count

    def get_badge_node_game_name(self, badge_node):
        # For testing
        # badge_title_text = badge_node.find("div", {"class": "badge_title"}).text
        # print(f"old: {repr(badge_title_text)}")
        # badge_title_text = re.sub("\n|\t|\r|View details|\xa0", "", badge_title_text)
        # print(f"new: {repr(badge_title_text)}")
        # return badge_title_text
        badge_title_text = badge_node.find("div", {"class": "badge_title"}).text
        return re.sub("\n|\t|\r|View details|\xa0", "", badge_title_text)

    def get_badge_node_game_id(self, badge_node):
        badge_link_node = badge_node.find("a", {"class": "badge_row_overlay"})
        if badge_link_node is None:
            return "0"
        badge_link = badge_link_node["href"]
        if "/gamecards/" not in badge_link:
            return "0"
        return badge_link.split("/gamecards/", 1)[1].replace("/", "")

    def _new_badge_dict(
        self, badge_id="0", badge_name="Badge Name", badge_drop_count=0
    ):
        return {"id": badge_id, "name": badge_name, "drop_count": badge_drop_count}
