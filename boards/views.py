import environ

env = environ.Env()

import requests
import xml.etree.ElementTree as ET  
from bs4 import BeautifulSoup
import json


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    PermissionDenied,
)
from django.contrib.auth.hashers import check_password


from .models import PossibleBoard
from .serializers import PossibleBoardSerializer, PossibleBoardListSerializer

# 하단 크롤링을 위한 정보
def parse_xml(xml_string):
    root = ET.fromstring(xml_string)

    items = root.findall(".//PatentUtilityInfo")
    data = []

    for item in items:
        result = {}
        # 발명 날짜
        result['ApplicationDate'] = item.find('ApplicationDate').text if item.find('ApplicationDate') is not None else None
        # 발명의 명칭
        result['InventionName'] = item.find('InventionName').text if item.find('InventionName') is not None else None
        # 발명자
        result['Applicant'] = item.find('Applicant').text if item.find('Applicant') is not None else None
        # 발명 현황
        result['RegistrationStatus'] = item.find('RegistrationStatus').text if item.find('RegistrationStatus') is not None else None
        data.append(result)
    return data


# 로그인 없이 게시글 작성 가능 / kipris 조회
class PossibleBoardWrite(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PossibleBoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            title = serializer.data["title"]
            words = title.replace(",", "").split()  # ,와 띄어쓰기 제거
            
            results = []

            access_key = env("access_key")
            kipris_url = "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/freeSearchInfo?word={word}&accessKey={access_key}"

            for word in words:
                url = kipris_url.format(word=word, access_key=access_key)
                response = requests.get(url)

                # xml 형식의 데이터를 파싱하고 원하는 정보를 추출하여 json 형식으로 저장
                data = parse_xml(response.text)

                results.extend(data) # 한번에 보여주는 방식
            
            # 모든 결과의 개수를 구함
            # total_count = sum(len(result) for result in results)
            # total_count = 0
            # for result in results:
            #     total_count+=len(result)
            
            total_count = len(results)
            
            
            global board
            board = {
                "title": title,
                "total_count": total_count,
                "results": results
            }
            
            return Response(board, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        global board
        if board is not None:
            return Response(board, status=200)
        else:
            return Response({"message":"데이터가 없습니다."}, status=204)
        

# 게시를 리스트
class PossibleBoardList(APIView):
    def get(self, request):
        possible_board = PossibleBoard.objects.all()
        serializer = PossibleBoardListSerializer(possible_board, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# 게시글 자세히 조회, 수정, 삭제 // 비밀번호로 확인
class PossibleBoardDetail(APIView):
    # 게시글 조회를 위해 필요한 부분
    def get_object(self, post_pk):
        try:
            return PossibleBoard.objects.get(pk=post_pk)
        except PossibleBoard.DoesNotExist:
            raise PermissionDenied("게시글을 찾을 수 없습니다.")

    # 비밀번호 체크
    def check_password(self, possible_board, password):
        if not check_password(password, possible_board.password):
            raise PermissionDenied("비밀번호가 일치하지 않습니다.")
    
    # 비밀번호 유효성 및 게시글 존재 여부 확인
    def validate_contents(self, request, post_pk):
        possible_board = self.get_object(post_pk)
        password = request.data.get("password")
        self.check_password(possible_board, password)
        return possible_board
    
    # 게시글 조회
    def get(self, request, post_pk):
        possible_board = self.validate_contents(request, post_pk)
        serializer = PossibleBoardSerializer(possible_board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시글 수정
    def put(self, request, post_pk):
        possible_board = self.validate_contents(request, post_pk)
        serializer = PossibleBoardSerializer(possible_board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, post_pk):
        possible_board = self.validate_contents(request, post_pk)
        possible_board.delete()
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)