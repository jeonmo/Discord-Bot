import booksearch

# 디스코드 도서검색 처리과정 함수
async def library_search(message, client):
    book_list_str, book = booksearch.book_list_search(message.content)

    if book_list_str != '':
        await message.channel.send(book + "의 검색 결과입니다.\n```" + book_list_str + '```' + '소장사항을 보길 원하는 도서의 번호를 입력해주세요.')

        input_no_msg = await client.wait_for('message', check=booksearch.book_check)
        input_no = input_no_msg.content # 사용자로부터 입력받은 메세지

        book_rental_msg = booksearch.book_rental_check(input_no)

        await message.channel.send(book_rental_msg)
    else :
        await message.channel.send('검색 결과가 없습니다.')