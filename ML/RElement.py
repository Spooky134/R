class RElement:
    status = 1

    def update_status(self, summ):
        if summ >= 0:
            self.status = 1
        else:
            self.status = 0

