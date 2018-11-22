$ = django.jQuery;
$(document).ready(function () {
    var Upload = function () {
        var obj = this;
        obj.url = '';
        obj.files = null;
        obj.init = function () {
            $('body').append('<form enctype="multipart/form-data" method="post" class="inline-uploadfiles-form"><input type="file" id="inline-uploadfiles-input" multiple></form>');
        };
        obj.getType = function (i) {
            return obj.files[i].type;
        };
        obj.getSize = function (i) {
            return obj.files[i].size;
        };
        obj.getName = function (i) {
            return obj.files[i].name;
        };
        obj.success = function (data) {
            window.location.reload();
        };
        obj.error = function (error_data) {

        };
        obj.xhr = function (percent) {
        };
        obj.doUpload = function () {
            var that = this;
            var formData = new FormData();

            for (var i = 0; i < obj.files.length; i++) {
                formData.append("uploadfiles[]", obj.files[i], obj.getName(i));
            }

            formData.append("upload_file", true);
            formData.append("csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val());

            $.ajax({
                    type: "POST",
                    url: obj.url,
                    xhr: function () {
                        var myXhr = $.ajaxSettings.xhr();
                        if (myXhr.upload) {
                            myXhr.upload.addEventListener('progress', that.progressHandling, false);
                        }
                        return myXhr;
                    },
                    success: function (data) {
                        obj.success(data);
                    },
                    error: function (error_data) {
                        obj.error(error_data);
                    },
                    async: true,
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    timeout: 60000
                }
            );
        };
        this.progressHandling = function () {
            var percent = 0;
            var position = event.loaded || event.position;
            var total = event.total;
            if (event.lengthComputable) {
                percent = Math.ceil(position / total * 100);
            }
            obj.xhr(percent);
        };
        $(document).on('click', '.inline-uploadfiles-link', function () {
            if (!$(this).hasClass('load')) {
                obj.url = $(this).data('uploadfiles')
                $('#inline-uploadfiles-input').click();
            }
        });
        $(document).on('change', '#inline-uploadfiles-input', function () {
            obj.files = $(this).get(0).files;
            obj.doUpload();
        });
        obj.init();
    };
    Upload();
});