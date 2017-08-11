from rest_framework import serializers
from .models import Questions, MarkingAlgo


class QuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ('id', 'question', 'answer', 'mark')
        # fields = '__all__'


class MarkingAlgoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarkingAlgo
        fields = ('qid', 'mark', 'point')
