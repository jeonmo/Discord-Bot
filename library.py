import booksearch

# 디스코드 도서검색 처리과정 함수
# 디스코드 봇과 사용자가 소통하는 도서검색 과정의 흐름을 나타낸 함수입니다.
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

async def library_collection(message, client):
    await message.channel.send("```동의대 콜랙션을 확인할 수 있습니다.\n원하는 번호를 선택해주세요.\n1. 베스트셀러\n2. 동의대권장도서\n3. 원북원부산도서\n4. 특성화(트렌드)도서\n5. 북큐레이션```")

    input_no_msg = await client.wait_for('message', check=collection_check)
    input_no = input_no_msg.content

    if input_no == '1':
        collection_msg = bookcollection.book_bestSeller()
        await message.channel.send(collection_msg)

    if input_no == '2':
        collection_msg = bookcollection.book_recommended()
        await message.channel.send(collection_msg)

    if input_no == '3':
        collection_msg = bookcollection.book_oneBookOneBusan()
        await message.channel.send(collection_msg)
    
    if input_no == '4':
        collection_msg = bookcollection.book_trend()
        await message.channel.send(collection_msg)
    
    if input_no == '5':
        collection_msg = bookcollection.book_bookCuration()
        await message.channel.send(collection_msg)

    

def collection_check(m): # 도서추천의 wait_for에 사용되는 check 함수
    return m.content
