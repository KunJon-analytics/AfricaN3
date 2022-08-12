from django.utils.encoding import smart_str
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from users.models import CustomUser
from words.models import Wordle, Word, Sitting, Winner
from users.api.serializers import UserSerializer

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class SittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitting
        fields = '__all__'

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = '__all__'

class WordleSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, write_only=True, required=False)
    master = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='wallet_address'
    )
    word = serializers.SerializerMethodField()

    class Meta:
        model = Wordle
        fields = '__all__'

    def create(self, validated_data):
        words_data = validated_data.pop('words')
        wordle = Wordle.objects.create(**validated_data)
        for word_data in words_data:
            Word.objects.create(wordle=wordle, **word_data)
        return wordle

    def get_word(self, obj):
        word = obj.words.filter(found = False).first()
        data = WordSerializer(word).data
        return data

class AddWordleSerializer(serializers.ModelSerializer):
    master = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='wallet_address'
    )

    class Meta:
        model = Wordle
        fields = '__all__'