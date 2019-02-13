document.addEventListener("DOMContentLoaded", function(){
  var playButtons = document.querySelectorAll('.video-container .play-button');
  playButtons.forEach(function(playButton) {
    playButton.addEventListener('click', function(event) {
      var playOverlay = event.target.parentNode;
      var consentOverlay = event.target.parentNode.parentNode.querySelector('.overlay-wrapper');
      playOverlay.classList.add('hide');
      consentOverlay.classList.remove('hide');

      /* Wait for the consent buttons to be visible before adding event listeners to it */
      var consentButtons = document.querySelectorAll('.overlay-wrapper button');
      consentButtons.forEach(function(consentButton) {
        consentButton.addEventListener('click', saveConsent);
      });
    });
  });

  var saveConsent = function(event) {
    var remember = event.target.parentNode.querySelector("[name='remember_decision']").checked;
    var provider = event.target.getAttribute('data-provider');
    var videoid = event.target.getAttribute('data-video');

    if (remember) {
        window.localStorage.setItem('allow_' + provider + '_embed', true);
    }

    var event = new Event('allow_all_' + provider);
    document.dispatchEvent(event);

    loadVideo(videoid, provider);
  };

  var hideBackdrop = function(container) {
    container.querySelector('img').classList.add('hide');
  };

  var loadVideo = function(videoid, provider) {
    var videoContainer = document.getElementById(videoid);
    var iframe = videoContainer.querySelector('iframe');
    iframe.setAttribute("src", iframe.getAttribute('data-url'));

    // Do the autoplay thing if possible/needed
    // This is for example the code used for vimeo
    // var script = document.createElement('script');
    // if(provider === "vimeo"){
    //   script.onload = function() {
    //     var player = new Vimeo.Player(iframe);
    //     player.play();
    //     player.on('play', hideBackdrop)
    //   }.bind(this);
    //   script.src = "https://player.vimeo.com/api/player.js";
    //   document.head.appendChild(script);
    // }
  };

  var initAllowed = function(isAllowed, provider) {
    var all_videos = document.querySelectorAll(".video-container[data-provider=" + provider + "]");
    all_videos.forEach(function(video){
      video.setAttribute('data-allowed', isAllowed);
      if(isAllowed) {
        var iframe = video.querySelector('iframe');
        iframe.setAttribute('src', iframe.getAttribute('data-url'));
      }
    });
  };

  /* initialize video for each provider (should the video banner be shown or not) */
  var providers = ['vimeo', 'youtube', 'dailymotion'];
  for(var i = 0; i < providers.length; i++) {
    document.addEventListener('allow_all_' + providers[i], function (e) {
      var provider = e.type.replace('allow_all_', '');
      initAllowed(true, provider);
    }, false);

    /* check if a decision has been made about the videos */
    var allowVideos = window.localStorage.getItem('allow_' + providers[i] + '_embed') || false;
    initAllowed(allowVideos, providers[i]);
  }
});
