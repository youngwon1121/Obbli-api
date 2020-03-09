class ResumeSerializer(serializers.ModelSerializer):
    selfie = serializers.ImageField(use_url=True, required=False)
    #fixed_selfie = serializers.SerializerMethodField()

    def to_internal_value(self, data):
        '''
        ret['selfie'] : InMemoryUploadedFile
        ret['selfie'].name
        ret['selfie'].content_type
        ret['selfie'].file : BytesIO
        '''        
        ret = super(ResumeSerializer, self).to_internal_value(data)
        if 'selfie' in ret:
            io = BytesIO()

            selfie = ret['selfie'].file
            im = Image.open(selfie)
            im = im.resize((200, 200))
            im.save(io, ret['selfie'].content_type.split('/')[-1].upper())

            ret['selfie'] = InMemoryUploadedFile(
                io,
                'photo',
                ret['selfie'].name,
                ret['selfie'].content_type,
                None, None
            )
        return ret

    class Meta:
        model = Profile
        read_only_fields = ('owner', )
        fields = ('owner', 'intro', 'selfie', 'id', )