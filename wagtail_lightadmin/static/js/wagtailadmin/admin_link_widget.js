function createLinkChooser(id, url, title) {
    var chooserElement = $('#' + id + '-chooser');
    var pageTitle = chooserElement.find('.chosen');
    var input = $('#' + id);

    $('.action-choose', chooserElement).click(function() {
        var initialUrl = window.chooserUrls.pageChooser;
        var title = title;
        var url = url;
        if (input.val()) {
            var old = JSON.parse(input.val());
            title = old.title;
            url = old.url;
        }
        var urlParams = {
            'allow_external_link': true,
            'allow_email_link': true,
            'can_choose_root': true,
            'link_text': title,
            'link_url': url
        };

        ModalWorkflow({
            url: initialUrl,
            urlParams: urlParams,
            responses: {
                pageChosen: function(pageData) {
                    input.val(JSON.stringify(pageData));
                    var link_title = pageTitle.find('input')[0];
                    link_title.setAttribute("aria-label", pageData.url);
                    link_title.title = pageData.url;
                    link_title.value = pageData.title;

                    chooserElement.removeClass('blank');
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        openAtParentId = null;
        chooserElement.addClass('blank');
    });

    var applyTitle = function(){
        if(input.val()){
            var old = JSON.parse(input.val());
            if (old.url) {
                old.title = pageTitle.find("input").val();
                input.val(JSON.stringify(old));
            }
        }
    };

    // Get the parent form
    $(input[0].form).on('submit', applyTitle);
    // Preview only works for page models anyways
    $('#page-edit-form').on("click", ".action-preview", applyTitle);

}
