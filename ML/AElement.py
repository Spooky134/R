
class AElement:
    lamdas = 1

    status = 1

    def update_status(self, image_array, connection):
        sum = 0
        for i in range(len(image_array)):
            sum += image_array[i] * connection[i]
        if sum >= 0:
            self.status = 1
        else:
            self.status = 0

