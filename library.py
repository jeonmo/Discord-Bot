import booksearch

# 디스코드 도서검색 처리과정 함수
# 디스코드 봇과 사용자가 소통하는 도서검색 과정의 흐름을 나타낸 함수입니다.
async def library_search(message, client, mainmsg):
    book_list_str, book = booksearch.book_list_search(message.content)

    if book_list_str != '':
        mainmsg = await mainmsg.edit(content = book + "의 검색 결과입니다.\n```" + book_list_str + '```' + '소장사항을 보길 원하는 도서의 번호를 입력해주세요.')

        input_no_msg = await client.wait_for('message', check=booksearch.book_check)
        input_no = input_no_msg.content # 사용자로부터 입력받은 메세지

        book_rental_msg = booksearch.book_rental_check(input_no)

        mainmsg = await mainmsg.edit(content = book_rental_msg)
    else :
        mainmsg = await mainmsg.send(content = '검색 결과가 없습니다.')
