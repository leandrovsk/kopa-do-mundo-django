from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from django.forms.models import model_to_dict
from teams.models import Team
from teams.utils import data_processing
from teams.exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)


class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        teams_list = []

        for team in teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)
        return Response(teams_list)

    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
        except NegativeTitlesError:
            return Response(
                {"error": "titles cannot be negative"},
                status.HTTP_400_BAD_REQUEST,
            )
        except InvalidYearCupError:
            return Response(
                {"error": "there was no world cup this year"},
                status.HTTP_400_BAD_REQUEST,
            )
        except ImpossibleTitlesError:
            return Response(
                {"error": "impossible to have more titles than disputed cups"},
                status.HTTP_400_BAD_REQUEST,
            )
        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)
