from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    PermissionDenied,
)
from django.contrib.auth.hashers import check_password
from taggit.models import Tag


from .models import PossibleBoard
from .serializers import PossibleBoardSerializer


# 로그인 없이 모두 작성 가능
class PossibleBoardWrite(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        keywords = request.data.get("keywords", "")
        keywords = keywords.split()  # split by space
        if len(keywords) > 5:
            return Response({"error": "키워드는 최대 5개까지만 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()  # request.data is immutable
        data["keywords"] = [keyword.strip() for keyword in keywords]

        serializer = PossibleBoardSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            instance.keywords.clear()
            for keyword in data["keywords"]:
                instance.keywords.add(keyword)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 조회, 수정, 삭제 // 비밀번호로 확인
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, post_pk):
        possible_board = self.validate_contents(request, post_pk)
        possible_board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)