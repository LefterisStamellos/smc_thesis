//console.clear();

$('#step1').hide();
$('#step2').hide();
$('#step3').hide();
$('#step4').hide();
$('#step5').hide();
$('#step6').hide();
$('#step7').hide();
$('#step8').hide();
$('#step9').hide();
$('#step10').hide();
$('#step11').hide();
$('#step12').hide();
$('#step13').hide();
$('#step14').hide();
$('#step15').hide();
$('#step16').hide();
$('#step17').hide();
$('#step18').hide();
$('#step19').hide();
$('#step20').hide();
$('#step21').hide();
$('#final').hide();

counter = 0;

var AUDIO = new(window.AudioContext || window.webkitAudioContext)();

var dispatcher = _.extend({
    'EventKeys': {},
    register: function(eventHash) {
        for (var k in eventHash) {
            if (k in this.EventKeys) throw 'Dispatcher error: duplicate event key: ' + k;

            this.EventKeys[k] = eventHash[k];
        }
    }
}, Backbone.Events);


/**
 * Sample bank.  Loads and maintains sound sources
 * and responds to requests to play them.
 **/
var SampleBank = (function(A) {

    var bank = {},
        loadCount = 0,
        totalCount = 0;

    /**
     * Resource loading
     **/

    function loadSamples(srcObj, callback) {
        for (var k in srcObj) {
            totalCount++;
        }
        for (var k in srcObj) {
            _loadSample(k, srcObj[k]);
        }
        _onSamplesLoaded = callback;
    }

    function _onSamplesLoaded() {
        console.warn('Need to pass a callback to load()');
    }

    function _handleSampleLoad(key, buffer) {
        if (!buffer) {
            console.error('Unable to decode audio file', url);
            return;
        }
        bank[key] = buffer;
        if (++loadCount == totalCount) _onSamplesLoaded();
    }

    function _loadSample(key, url) {
        var req = new XMLHttpRequest();
        req.responseType = "arraybuffer";
        req.onload = function() {
            A.decodeAudioData(req.response, function(b) {
                _handleSampleLoad(key, b);
            }, function(err) {
                console.error('Unable to decode audio data', err);
            });
        }
        req.onerror = function(err) {
            console.error('Error loading sample data', key, url, err);
        }
        req.open('GET', url, true);
        req.send();
    }

    /**
     * Resource playing
     **/

    function playSample(id, when) {
        var s = A.createBufferSource();
        s.buffer = bank[id];
        s.connect(A.destination);
        s.start(when || 0);
    }

    var API = {
        play: playSample,
        init: loadSamples
    };
    return API;

})(AUDIO);







/**
 * Sequencer
 **/
var Sequencer = (function(A, S) {

    var evs = {
        SEQUENCER_PLAY: 'sequencer:play',
        SEQUENCER_STOP: 'sequencer:stop',
        SEQUENCER_SET_PATTERN: 'sequencer:setpattern',
        SEQUENCER_PATTERN_CHANGED: 'sequencer:patternchanged',
        SEQUENCER_STEP: 'sequencer:step',
        SEQUENCER_NOTE_PLAY: 'sequencer:noteplay'
    };

    var tempo, tic, _initialized = false;
    var noteTime, startTime, ti, currentStep = 0;
    var isPlaying = false;
    var currentPattern = null,
        _currentPatternSequenceRaw;
    var channelStatus = {};

    function setTempo(newTempo) {
        tempo = newTempo;
        tic = (60 / tempo) / 4; // 16th
    }

    /* Scheduling */

    function scheduleNote() {
        if (!isPlaying) return false;
        var ct = A.currentTime;
        ct -= startTime;
        while (noteTime < ct + 0.200) {
            var pt = noteTime + startTime;

            playPatternStepAtTime(pt);

            nextNote();
        }
        ti = setTimeout(scheduleNote, 0);
    }

    function nextNote() {
        currentStep++;
        if (currentStep == 16) currentStep = 0;
        noteTime += tic;
    }

    function playPatternStepAtTime(pt) {
        for (var k in currentPattern) {
            if (channelStatus[k] !== false && currentPattern[k][currentStep] == "1") {
                S.play(k, pt);
                dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_NOTE_PLAY, k);
            }
            dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_STEP, currentStep);
        }
    }

    /* Parsing */

    function playPattern(pattern, loops) {
        if (!_initialized) throw ('Sequencer not initialized');
        if (currentPattern === null) _parsePattern(pattern);

        if (loops === undefined) loops = 1;
        if (loops === -1) loops = Number.MAX_INT;

        play();
    }

    function _parsePattern(pattern) {
        currentPattern = {};
        _currentPatternSequenceRaw = _.extend(pattern.sequence, {});
        for (var k in pattern.sequence) {
            var pat = _parseLine(pattern.sequence[k]);
            currentPattern[k] = pat;
        }
    }

    function _parseLine(line) {
        if (line.length !== 16) console.error('Invalid line length', pattern);
        return line.split('');
    }

    /** Transport **/

    function play() {
        isPlaying = true;
        noteTime = 0.0;
        startTime = A.currentTime + 0.005;
        scheduleNote();
    }

    function stop() {
        isPlaying = false;
        currentStep = 0;
        dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_STEP, currentStep);
    }

    function changeChannelActiveStatus(channel, status) {
        channelStatus[channel] = status;
    }

    var _template = Handlebars.compile('\
    <div class="module sequencer">\
      <h3>Sequencer</h3>\
      <div class="sequencer-channels">\
            {{#each channels}}\
                <div class="channel" data-inst="{{ this }}"></div>\
                <div class="sep"></div>\
            {{/each}}\
            </div>\
    </div>');

    var SequencerView = Backbone.View.extend({

        channelViews: {},
        initialize: function(options) {
            this.listenTo(dispatcher, dispatcher.EventKeys.SEQUENCER_PLAY, playPattern);
            this.listenTo(dispatcher, dispatcher.EventKeys.SEQUENCER_STOP, this.stop);
            this.listenTo(dispatcher, dispatcher.EventKeys.SEQUENCER_SET_PATTERN, this.setPattern);
            this.listenTo(dispatcher, dispatcher.EventKeys.SEQUENCER_SET_TEMPO, setTempo);
            this.listenTo(dispatcher, dispatcher.EventKeys.SEQUENCER_STEP, this.setPlayhead);
            this.listenTo(dispatcher, dispatcher.EventKeys.SEQUENCER_NOTE_PLAY, this.onNotePlay);
        },
        setPattern: function(pattern) {
            _parsePattern(pattern);

            this.render();

            for (var k in this.channelViews) {
                this.channelViews[k].remove();
            }
            for (var k in currentPattern) {
                var $cel = this.$el.find('.channel[data-inst="' + k + '"]');
                this.channelViews[k] = new ChannelView({
                    channel: k,
                    model: currentPattern[k],
                    el: $cel
                });
            }

            this.renderChannels();
        },
        render: function() {
            var data = (currentPattern) ? Object.keys(currentPattern) : [];
            var rawHTML = _template({
                channels: data
            });
            this.$el.html(rawHTML);
            return this;
        },
        renderChannels: function() {
            this.$channelContainer = this.$el.find('.sequencer-channels');
            for (var k in this.channelViews) {
                this.channelViews[k].render();
            }
            this.$steps = $('.channel span');
        },
        setPlayhead: function(stepId) {
            for (var k in this.channelViews) {
                this.channelViews[k].setPlayhead(stepId);
            }
        },
        onNotePlay: function(channel) {
            this.channelViews[channel].spikeEQ();
        },
        stop: function() {
            stop();
            for (var k in this.channelViews) {
                this.channelViews[k].clearPlayhead();
            }
        }
    });

    var _channelTemplate = Handlebars.compile('\
      <button class="control mute active"></button>\
      <button class="control pad">{{ symbol }}</button>\
      <div class="control meter vertical">\
        <span></span>\
      </div>\
      <div class="seq-row inline">\
        {{#each notes}}\
        <span data-tic="{{ @index }}" class=""></span>\
                {{/each}}\
      </div>\
    ');

    var ChannelView = Backbone.View.extend({
        events: {
            'click .seq-row span': 'onNoteClick',
            'click .pad': 'onPadClick',
            'click .mute': 'onMuteClick'
        },
        channel: null,
        active: true,
        initialize: function(options) {
            this.channel = options.channel;
        },
        render: function() {
            var rawHTML = _channelTemplate({
                id: this.channel,
                // symbol: this.channel.toUpperCase(),
                symbol: this.channel.substr(0, 1).toUpperCase(),
                notes: this.model
            });
            this.$el.html(rawHTML);

            this.$notes = this.$el.find('.seq-row span');
            this.$eq_bar = this.$el.find('.meter span');
            this.$active = this.$el.find('.mute');

            var self = this;
            this.model.forEach(function(note, idx) {
                var $el = self.$notes.eq(idx);
                if (note === "1") $el.addClass('seq-note');
                if (idx % 4 === 0) $el.addClass('seq-step-measure');
            });
            this.spikeEQ();
            this.$active.toggleClass('active', this.active);
            return this;
        },
        clearPlayhead: function() {
            this.$notes.removeClass('seq-playhead');
        },
        setPlayhead: function(id) {
            this.clearPlayhead();
            this.$notes.filter('[data-tic="' + id + '"]').addClass('seq-playhead');
        },
        onNoteClick: function(e) {
            var tic = $(e.currentTarget).attr('data-tic');
            currentPattern[this.channel][tic] = (currentPattern[this.channel][tic] === "1") ? "0" : "1";
            this.render();
        },
        onMuteClick: function(e) {
            this.active = !this.active;
            channelStatus[this.channel] = this.active;
            this.$active.toggleClass('active', this.active);
        },
        onPadClick: function(e) {
            S.play(this.channel);
            this.spikeEQ(this.channel);
        },
        spikeEQ: function() {

            var self = this;
            this.$eq_bar.removeClass('fade');
            this.$eq_bar.css('transform', 'scaleX(1)');

            setTimeout(function() {
                self.$eq_bar.addClass('fade');
                self.$eq_bar.css('transform', 'scaleX(0)');
            }, 50);
        }
    });

    function init(options) {
        dispatcher.register(evs);
        new SequencerView(options).render();
        setTempo(130);
        _initialized = true;
    }

    return {
        init: init
    }

})(AUDIO, SampleBank);







/**
 * Transport
 **/
var Transport = (function() {

    var evs = {
        TRANSPORT_PLAY: 'transport:play',
        TRANSPORT_STOP: 'transport:stop',
        TRANSPORT_REQUEST_PLAY: 'transport:requestplay',
        TRANSPORT_REQUEST_STOP: 'transport:requeststop',
        TRANSPORT_TEMPO_CHANGED: 'transport:tempochanged',
        TRANSPORT_CHANGE_TEMPO: 'transport:changetempo'
    }

    var _template = Handlebars.compile('\
    <div class="module transport">\
      <h3>Transport</h3>\
      <button class="transport-play" title="Play">&#9658;</button>\
            <button class="transport-stop" title="Stop">&#9632;</button>\
            <input type="text" size="3" min="30" max="250" value="130" class="transport-tempo" /> \
    </div>\
  ');

    function play() {
        //console.log('play');
        dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_REQUEST_PLAY);
    }

    function stop() {
        dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_REQUEST_STOP);
    }

    var TransportView = Backbone.View.extend({
        events: {
            'click .transport-play': 'onPlayClick',
            'click .transport-stop': 'onStopClick',
            'change .transport-tempo': 'onTempoChange'
        },
        initialize: function(options) {
            this.listenTo(dispatcher, dispatcher.EventKeys.TRANSPORT_PLAY, play);
            this.listenTo(dispatcher, dispatcher.EventKeys.TRANSPORT_STOP, stop);
            this.listenTo(dispatcher, dispatcher.EventKeys.TRANSPORT_CHANGE_TEMPO, this.onIncomingTempoChange);
        },
        render: function() {
            var rawHTML = _template();
            this.$el.html(rawHTML);
            this.$tempo = this.$el.find('.transport-tempo');
            return this;
        },
        onPlayClick: play,
        onStopClick: stop,
        onTempoChange: function(e) {
            var newTempo = $(e.currentTarget).val();
            dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_TEMPO_CHANGED, newTempo);
        },
        onIncomingTempoChange: function(newTempo) {
            this.$tempo.val(newTempo);
            dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_TEMPO_CHANGED, newTempo);
        }
    });

    function init(options) {
        dispatcher.register(evs);
        new TransportView(options).render();
    }

    return {
        init: init
    }

})();







/**
 * Metronome
 **/
var Metronome = (function() {

    var evs = {
        METRONOME_TIC: 'metronome:tic',
        METRONOME_CLEAR: 'metronome:clear'
    }

    var _template = Handlebars.compile('\
        <h3>Metronome</h3>\
        <div class="control metronome">\
      <span></span>\
      <span></span>\
      <span></span>\
      <span></span>\
    </div>\
    ');

    var MetronomeView = Backbone.View.extend({
        initialize: function(options) {
            this.listenTo(dispatcher, dispatcher.EventKeys.METRONOME_TIC, this.onTic);
            this.listenTo(dispatcher, dispatcher.EventKeys.METRONOME_CLEAR, this.clear);
        },
        render: function() {
            var rawHTML = _template();
            this.$el.html(rawHTML);
            this.$steps = this.$el.find('span');
            return this;
        },
        clear: function() {
            this.$steps.removeClass('active');
        },
        onTic: function(stepId) {
            if (stepId % 4 == 0) {
                this.clear();
                this.$steps.eq(Math.floor(stepId / 4)).addClass('active');
            }
        }
    });

    function init(options) {
        dispatcher.register(evs);
        new MetronomeView(options).render();
    }

    return {
        init: init
    }
})();






/**
 * Preset pattern selector
 **/
// var PresetList = (function() {

//     var evs = {
//         PRESET_SELECTED: 'preset:selected'
//     }

//     var presets = {
//         'remaining': {
//             tempo: 100,
//             name: 'Remaining',
//             sequence: {
//                 'openHat': '0010001000100010',
//                 'closedHat': '1000100010001000',
//                 'snare': '0000100000001000',
//                 'kick': '1000000010100100'
//             }
//         },
//         'coagulate': {
//             tempo: 124,
//             name: 'Coagulate',
//             sequence: {
//                 'openHat': '0010000000000010',
//                 'closedHat': '1100111111111100',
//                 'snare': '0000100000001000',
//                 'kick': '0110000010000001'
//             }
//         },
//         'deodorize': {
//             tempo: 118,
//             name: 'Deodorize',
//             sequence: {
//                 'openHat': '1000100010001000',
//                 'closedHat': '0000000000000000',
//                 'snare': '0000100101001000',
//                 'kick': '1001000000110100'
//             }
//         },
//         'maintain': {
//             tempo: 90,
//             name: 'Maintain',
//             sequence: {
//                 'openHat': '0000000000100000',
//                 'closedHat': '1010101010001010',
//                 'snare': '0000100000001000',
//                 'kick': '0010010010000010'
//             }
//         },
//         'mufuh': {
//             tempo: 130,
//             name: 'Mufu',
//             sequence: {
//                 'openHat': '0011000000000110',
//                 'closedHat': '1100111111111001',
//                 'snare': '0000100101001101',
//                 'kick': '1010000000100000'
//             }
//         },
//         'gabriel': {
//             tempo: 135,
//             name: 'Gabriel',
//             sequence: {
//                 'openHat': '0000000000010000',
//                 'closedHat': '0000011000000100',
//                 'snare': '0000109000001000',
//                 'kick': '1000010100100000'
//             }
//         },
//         'empty': {
//             tempo: 130,
//             name: '[empty]',
//             sequence: {
//                 'openHat': '0000000000000000',
//                 'closedHat': '0000000000000000',
//                 'snare': '0000000000000000',
//                 'kick': '0000000000000000'
//             }
//         }
//     };

//     var _template = Handlebars.compile('\
//      <h3>Presets</h3>\
//      <ul class="control presets menu">\
//      {{#each items}}\
//      <li><a href="#" data-preset-id="{{ @key }}">{{ name }}</a></li>\
//     {{/each}}\
//     </ul>\
//  ');

//     var PresetListView = Backbone.View.extend({
//         events: {
//             'click a': 'onPresetClick'
//         },
//         render: function() {
//             var rawHTML = _template({
//                 items: presets
//             });
//             this.$el.html(rawHTML);
//             this.$items = this.$el.find('a');
//             return this;
//         },
//         onPresetClick: function(e) {
//             var id = $(e.currentTarget).attr('data-preset-id');
//             this.$items.removeClass('active');
//             $(e.currentTarget).addClass('active');
//             dispatcher.trigger(dispatcher.EventKeys.PRESET_SELECTED, presets[id]);
//         }
//     });

//     function init(options) {
//         dispatcher.register(evs);
//         new PresetListView(options).render();
//     }

//     return {
//         init: init
//     }

// })();


/** Application **/

var App = {

    _connectModules: function() {

        // Transport controls -> sequencer
        dispatcher.on(dispatcher.EventKeys.TRANSPORT_REQUEST_PLAY, function() {
            dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_PLAY);
        });
        dispatcher.on(dispatcher.EventKeys.TRANSPORT_REQUEST_STOP, function() {
            dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_STOP);
        });
        dispatcher.on(dispatcher.EventKeys.TRANSPORT_TEMPO_CHANGED, function(newTempo) {
            dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_SET_TEMPO, newTempo);
        });

        // Sequencer actions -> metronome
        dispatcher.on(dispatcher.EventKeys.SEQUENCER_STEP, function(stepId) {
            dispatcher.trigger(dispatcher.EventKeys.METRONOME_TIC, stepId);
        });
        dispatcher.on(dispatcher.EventKeys.SEQUENCER_STOP, function() {
            dispatcher.trigger(dispatcher.EventKeys.METRONOME_CLEAR);
        });

        // Preset list -> tempo and sequencer
        dispatcher.on(dispatcher.EventKeys.PRESET_SELECTED, function(preset) {
            dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_CHANGE_TEMPO, preset.tempo);
            dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_SET_PATTERN, preset);
        });

    },

    onLoad: function() {
        // console.log('passed: ', splurt)
        Sequencer.init({
            el: $('#r-mid')
        });
        Transport.init({
            el: $('#r-top')
        });
        Metronome.init({
            el: $('#r-head')
        });
        // PresetList.init({
        //     el: $('#r-footer')
        // });
        this._connectModules();

        // var pattern = {
        //     sequence: {
        //         'openHat': '0000000000000000',
        //         'closedHat': '0000000000000000',
        //         'snare': '0000100000001000',
        //         'kick': '1000000010000000',

        //     }
        // };

        //    dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_SET_PATTERN, pattern);
        //dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_PLAY);
    },

    init: function(randomBank) {
        //
        document.addEventListener('visibilitychange', function(e) {
            if (document.hidden) dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_STOP);
        }, false);

        var samples = randomBank;

        // Load samples and kickoff
        SampleBank.init(samples, this.onLoad.bind(this));
    },

    play: function(pattern) {
        dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_SET_PATTERN, pattern);
        dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_PLAY);
    },

    stop: function() {
        dispatcher.trigger(dispatcher.EventKeys.TRANSPORT_STOP);
    }
}

//App.init();
$('#app').hide();
var presets = {
    'first': {
        tempo: 100,
        name: 'first',
        sequence: {
                 'kick': '1010000000110000',
                 'snare': '0000100101001001',
                 'hihat': '0000000000000000',
                 'crash': '0000000000000000',
                 'ride': '1010101010101010',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },
    'second': {
        tempo: 124,
        name: 'second',
  sequence: {
                'kick': '1100000000000100',
                 'snare': '0000100000001000',
                 'hihat': '0010001000100010',
                 'crash': '0000000000000000',
                 'ride': '0000000000000000',
                 'rim': '0000000000000000',
                 'tom': '0000000000000011',
            }
    },
    'third': {
        tempo: 130,
        name: 'third',
  sequence: {
                 'kick': '1000001010000100',
                 'snare': '0000100000101000',
                 'hihat': '0000000000000000',
                 'crash': '1000000000000000',
                 'ride': '1000101101011000',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },
    'fourth': {
        tempo: 124,
        name: 'fourth',
  sequence: {
                 'kick': '1001001010010010',
                 'snare': '0100100010000111',
                 'hihat': '0000000000000000',
                 'crash': '1000000000000000',
                 'ride': '1001001001001001',
                 'rim': '0000000000000000',
                 'tom': '0000000000000111',
            }
    },
    'fifth': {
        tempo: 120,
        name: 'fifth',
  sequence: {
                 'kick': '0000000010000110',
                 'snare': '0100101100001000',
                 'hihat': '0000000000101010',
                 'crash': '0000000010000000',
                 'ride': '1011010000000000',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },
    'sixth': {
        tempo: 100,
        name: 'sixth',
  sequence: {
                 'kick': '1000100010001000',
                 'snare': '0000000000000000',
                 'hihat': '0010001000100010',
                 'crash': '0000000000000000',
                 'ride': '1001100110011001',
                 'rim': '0100001000000000',
                 'tom': '0001100001001100',
            }
    },

    'seventh': {
        tempo: 112,
        name: 'seventh',
  sequence: {
                 'kick': '1001010000001100',
                 'snare': '0010001000100010',
                 'hihat': '0000000000000000',
                 'crash': '0000000000000000',
                 'ride': '0000000000000000',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },

    'eighth': {
        tempo: 112,
        name: 'eighth',
  sequence: {
                 'kick': '1011010010110100',
                 'snare': '0000100100001001',
                 'hihat': '1000100010001000',
                 'crash': '0000000000000000',
                 'ride': '0000000000000000',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },

    'nineth': {
        tempo: 160,
        name: 'nineth',
  sequence: {
                 'kick': '1000001000100000',
                 'snare': '0000100000001000',
                 'hihat': '1000100010001000',
                 'crash': '0000000000000000',
                 'ride': '0000000000000000',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },

    'tenth': {
        tempo: 120,
        name: 'tenth',
  sequence: {
                 'kick': '1010000010100000',
                 'snare': '0000000000000000',
                 'hihat': '1010101010101010',
                 'crash': '0000000000000000',
                 'ride': '0000000000000000',
                 'rim': '1000100010001000',
                 'tom': '0000000000000000',
            }
    },
}

var isPlaying = false;
var drumItems = ['snare', 'kick', 'hihat', 'crash', 'ride', 'rim', 'tom'];
var answers = {};
var steps
var sounds_from_clfr = (function() {
        var sounds_from_clfr = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': "/static/js/clfr_drumsounds.json",
            'dataType': "json",
            'success': function (data) {
                sounds_from_clfr = data;
            }
        });
        return sounds_from_clfr;
    })();

var random_sounds = (function() {
        var random_sounds = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': "/static/js/rand_drumsounds.json",
            'dataType': "json",
            'success': function (data) {
                random_sounds = data;
            }
        });
        return random_sounds;
    })();

console.log('json file with sounds from classifier: ',sounds_from_clfr)
console.log('json file with random sounds: ',random_sounds)

data = sounds_from_clfr[0];
console.log('1st learned sequencer initialized with following data: ',data)
App.init(data)

$.get( "http://LefterisStamellos.pythonanywhere.com/stepsorder/", function( data ) {
    steps = data
});

$("#step0").submit(function(event) {
    event.preventDefault();
    $('#step0').hide();
    $('#step1').show();
});

$("#step1").submit(function(event) {
    event.preventDefault();

    var step1 = {
        train: $("input[name='train']:checked").val(),
        compose: $("input[name='compose']:checked").val(),
        perc: $("input[name='perc']:checked").val(),
    }

    answers.step1 = step1;

    console.log('answers: ', answers);
    console.log('steps: ',steps);

    $('#step1').hide();
    $('#step2').show();
});

$("#step2").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step2 = {
        question1: $("input[name='likert1']:checked").val(),
        question2: $("input[name='likert2']:checked").val(),
        question3: $("input[name='likert3']:checked").val(),
    }
    answers.step2 = step2;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step2').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});


$("#step3").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step3 = {
        question1: $("input[name='likert4']:checked").val(),
        question2: $("input[name='likert5']:checked").val(),
        question3: $("input[name='likert6']:checked").val(),
    }
    answers.step3 = step3;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step3').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step4").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step4 = {
        question1: $("input[name='likert7']:checked").val(),
        question2: $("input[name='likert8']:checked").val(),
        question3: $("input[name='likert9']:checked").val(),
    }
    answers.step4 = step4;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step4').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step5").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step5 = {
        question1: $("input[name='likert10']:checked").val(),
        question2: $("input[name='likert11']:checked").val(),
        question3: $("input[name='likert12']:checked").val(),
    }
    answers.step5 = step5;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step5').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step6").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step6 = {
        question1: $("input[name='likert13']:checked").val(),
        question2: $("input[name='likert14']:checked").val(),
        question3: $("input[name='likert15']:checked").val(),
    }
    answers.step6 = step6;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step6').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step7").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step7 = {
        question1: $("input[name='likert16']:checked").val(),
        question2: $("input[name='likert17']:checked").val(),
        question3: $("input[name='likert18']:checked").val(),
    }
    answers.step7 = step7;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step7').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step8").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step8 = {
        question1: $("input[name='likert19']:checked").val(),
        question2: $("input[name='likert20']:checked").val(),
        question3: $("input[name='likert21']:checked").val(),
    }
    answers.step8 = step8;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step8').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step9").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step9 = {
        question1: $("input[name='likert22']:checked").val(),
        question2: $("input[name='likert23']:checked").val(),
        question3: $("input[name='likert24']:checked").val(),
    }
    answers.step9 = step9;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step9').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step10").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step10 = {
        question1: $("input[name='likert25']:checked").val(),
        question2: $("input[name='likert26']:checked").val(),
        question3: $("input[name='likert27']:checked").val(),
    }
    answers.step10 = step10;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step10').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step11").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step11 = {
        question1: $("input[name='likert28']:checked").val(),
        question2: $("input[name='likert29']:checked").val(),
        question3: $("input[name='likert30']:checked").val(),
    }
    answers.step11 = step11;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step11').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step12").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step12 = {
        question1: $("input[name='likert31']:checked").val(),
        question2: $("input[name='likert32']:checked").val(),
        question3: $("input[name='likert33']:checked").val(),
    }
    answers.step12 = step12;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step12').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});


$("#step13").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step13 = {
        question1: $("input[name='likert34']:checked").val(),
        question2: $("input[name='likert35']:checked").val(),
        question3: $("input[name='likert36']:checked").val(),
    }
    answers.step13 = step13;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step13').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step14").submit(function(event) {
    App.stop();
    isPlaying = false
    event.preventDefault();

    var step14 = {
        question1: $("input[name='likert37']:checked").val(),
        question2: $("input[name='likert38']:checked").val(),
        question3: $("input[name='likert39']:checked").val(),
    }
    answers.step14 = step14;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step14').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step15").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step15 = {
        question1: $("input[name='likert40']:checked").val(),
        question2: $("input[name='likert41']:checked").val(),
        question3: $("input[name='likert42']:checked").val(),
    }
    answers.step15 = step15;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step15').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step16").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step16 = {
        question1: $("input[name='likert43']:checked").val(),
        question2: $("input[name='likert44']:checked").val(),
        question3: $("input[name='likert45']:checked").val(),
    }
    answers.step16 = step16;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step16').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step17").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step17 = {
        question1: $("input[name='likert46']:checked").val(),
        question2: $("input[name='likert47']:checked").val(),
        question3: $("input[name='likert48']:checked").val(),
    }
    answers.step17 = step17;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step17').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step18").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step18 = {
        question1: $("input[name='likert49']:checked").val(),
        question2: $("input[name='likert50']:checked").val(),
        question3: $("input[name='likert51']:checked").val(),
    }
    answers.step18 = step18;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step18').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step19").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step19 = {
        question1: $("input[name='likert52']:checked").val(),
        question2: $("input[name='likert53']:checked").val(),
        question3: $("input[name='likert54']:checked").val(),
    }
    answers.step19 = step19;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step19').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step)

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step20").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step20 = {
        question1: $("input[name='likert55']:checked").val(),
        question2: $("input[name='likert56']:checked").val(),
        question3: $("input[name='likert57']:checked").val(),
    }
    answers.step20 = step20;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step20').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#step21").submit(function(event) {
    App.stop();
    isPlaying = false;
    event.preventDefault();

    var step21 = {
        question1: $("input[name='likert58']:checked").val(),
        question2: $("input[name='likert59']:checked").val(),
        question3: $("input[name='likert60']:checked").val(),
    }
    answers.step21 = step21;

    console.log('answers: ', answers);
    console.log('steps: ',steps)

    $('#step21').hide();
    next_step = steps[Object.keys(steps)[0]];
    delete steps[Object.keys(steps)[0]];
    if (next_step == null){
        $('#final').show()
    }else{
        if (next_step<12){
            data = sounds_from_clfr[next_step-2];
            App.init(data)
            console.log('sounds: ',data)
        }else{
            data = random_sounds[next_step-12];
            App.init(data)
            console.log('sounds: ',data)
        }
        console.log('next step: ',next_step);

        console.log('counter: ',counter);
        counter = counter+1
        // // document.getElementById("myCounter").innerHTML=counter + "/20";
        //document.getElementById("myCounter").innerHTML="test";

        setTimeout(function(){
        $('#step'+next_step).show();
        }, 0);
        }
});

$("#final").submit(function(event) {
    $.ajax({
        type: "POST",
        url: "/finalize/",
        dataType: "json",
        data: JSON.stringify(answers, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result)
        }
    });
    $('#final').hide();
});

$("#first-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.second);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#second-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.second);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#third-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.third);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#fourth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.fourth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#fifth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.fifth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#sixth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.sixth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#seventh-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.seventh);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#eighth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.eighth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#nineth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.nineth);
        }, 900);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#tenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.tenth);
        }, 900);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#eleventh-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.second);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#twelveth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.third);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#thirteenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.fourth);
        }, 900);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#fourteenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.fifth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#fifteenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.sixth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#sixteenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.seventh);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#seventeenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.eighth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#eighteenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.nineth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#nineteenth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.tenth);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});

$("#twentieth-loop").click(function() {
    if (!isPlaying) {
        setTimeout(function(){
        App.play(presets.first);
        }, 700);
    } else {
        App.stop();
    }
    isPlaying = !isPlaying
    $(this).toggleClass("paused");
});