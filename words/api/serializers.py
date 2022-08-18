from rest_framework import serializers
from words.models import Letter, Wordle, Word, Sitting, Winner
from users.models import CustomUser

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class SittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitting
        fields = '__all__'

class WinnerSerializer(serializers.ModelSerializer):
    sitting = SittingSerializer(many=False, required=True)
    wordle_id = serializers.SerializerMethodField()

    class Meta:
        model = Winner
        fields = '__all__'

    def get_wordle_id(self, obj):
        data = obj.sitting.word.wordle.wordle_id
        return data

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ("key",)

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
        read_only=False,
        slug_field='wallet_address',
        queryset = CustomUser.objects.all()
    )

    class Meta:
        model = Wordle
        fields = '__all__'

class SittingWinnerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='wallet_address',
        queryset = CustomUser.objects.all()
    )

    class Meta:
        model = Sitting
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            winner = instance.winner
            representation['winner'] = True
        except Winner.DoesNotExist:
            representation['winner'] = False
        return representation

class WordleSittingsSerializer(serializers.ModelSerializer):
    sittings = serializers.SerializerMethodField()

    class Meta:
        model = Wordle
        fields = '__all__'

    def get_sittings(self, obj):
        sits = Sitting.objects.filter(word__wordle__pk=obj.pk)
        data = SittingWinnerSerializer(sits, many=True).data
        return data

    