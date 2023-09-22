from utils import check_section

class User:
    def __init__(self,account):
        self.account = account
        self.all_data = []
        self.result = {
            'tasks': {
                'Sunshine': [],
                'Boardgames': [],
                'Nightsky': [],
                'Unknown': []},
            'reviews': {
                'Sunshine': [],
                'Boardgames': [],
                'Nightsky': [],
                'Unknown': []}
        }
        self.time = 0

    def fill_result(self):
        for data in self.all_data:
            try:
                section = check_section(data['mnear_per_review'] / 1000)
                if data['performed_by'] == self.account:
                    self.result['tasks'][section].append(data['mnear_per_task'] / 1000)
                elif self.account in data['reviewers']:
                    self.result['reviews'][section].append(data['mnear_per_review'] / 1000)
            except:
                pass
        return self.result


