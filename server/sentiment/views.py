from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import analyze_text_sentiment


class SentimentAnalysisView(APIView):
    """
    POST /api/analyze-review/
    Accepts JSON body:
      {"text": "Fantastic services"} or {"review": "Fantastic services"}
    Returns:
      {
        "status": "success",
        "text": "Fantastic services",
        "sentiment": "positive",
        "score": 0.765,
        "label": "positive"
      }
    """

    def post(self, request):
        text = (
            request.data.get("text")
            or request.data.get("review")
            or request.data.get("message")
        )

        if text is None:
            return Response(
                {"error": "Field 'text' or 'review' is required in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        text_str = str(text)
        result = analyze_text_sentiment(text_str)

        response_data = {
            "status": "success",
            "text": text_str,
            "sentiment": result["sentiment"],
            "score": result["score"],
            "label": result["label"],
            "details": result.get("details", {}),
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def get(self, request):
        """Allow query param: /api/analyze-review/?text=Fantastic+services"""
        text = request.query_params.get("text") or request.query_params.get("review")
        if not text:
            return Response(
                {"error": "Query parameter 'text' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = analyze_text_sentiment(text)
        return Response(
            {
                "status": "success",
                "text": text,
                "sentiment": result["sentiment"],
                "score": result["score"],
                "label": result["label"],
            },
            status=status.HTTP_200_OK,
        )
