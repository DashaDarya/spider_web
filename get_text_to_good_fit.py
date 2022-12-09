
class TextGoodFit:
    @staticmethod
    def get_text_to_good_fit(text):
        text = str(text)
        text = text.split("doc")
        text_list = []

        # первая строка с количеством ссылок добавляется title
         # нужно найти строку в списке с Result и вытащить число ссылок и удалить эту строку

        for string in text:
            if "Result" in string:
                num = TextGoodFit.get_number(string)
                i = text.index(string)
                del text[i]
                break

        # удалить строку с Document

        for string in text:
            if "Document" in string:
                i = text.index(string)
                del text[i]
                break

        # в каждой оставшейся строке вытащить url и body

        for string in text:
            url_string = string.split("url",)
            url_string = url_string[1]
            item_list = url_string.split("body")

            url_string = item_list[0]
            body_string =item_list[1]


            i = text.index(string)
            del text[i]
            text_list.append((url_string, body_string))
            


        return text_list, num

    @staticmethod
    def get_number(string) -> str:
        l = len(string)
        print(string)
        # integ = []
        i = 0
        s_int = ''
        while i < l:
            a = string[i]
            while '0' <= a <= '9':
                s_int += a
                i += 1
                if i < l:
                    a = string[i]
                else:
                    break
            i += 1
        return s_int



        