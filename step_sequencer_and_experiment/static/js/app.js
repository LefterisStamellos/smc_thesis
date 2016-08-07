console.clear();

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
        setTempo(136);
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
      <input type="text" size="3" min="30" max="250" value="136" class="transport-tempo" /> \
    </div>\
  ');

    function play() {
        console.log('play');
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
var PresetList = (function() {

    var evs = {
        PRESET_SELECTED: 'preset:selected'
    }

    var presets = {
    'Funky Drummer': {
        tempo: 100,
        name: 'Funky Drummer',
        sequence: {
                 'kick': '1010000000110000',
                 'snare': '0000100101001001',
                 'hihat': '0000000000000000',
                 'crash': '0000000000000000',
                 'ride': '1111111111111111',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }
    },

    'Dance, Dance': {
        tempo: 112,
        name: 'Dance, Dance',
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

    'Immigrant Song': {
        tempo: 112,
        name: 'Immigrant Song',
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

    'Hey Ya!': {
        tempo: 160,
        name: 'Hey Ya!',
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

    'By The Way': {
        tempo: 120,
        name: 'By The Way',
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
    'Pupucha Incha': {
        tempo: 124,
        name: 'Pupucha Incha',
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
    'Amen Break': {
        tempo: 136,
        name: 'Amen Break',
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
    'Daedalus': {
        tempo: 124,
        name: 'Daedalus',
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
    'Paradiddle': {
        tempo: 120,
        name: 'Paradiddle',
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
    'Samba!': {
        tempo: 100,
        name: 'Samba!',
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
}

    var _template = Handlebars.compile('\
    <h3>Presets</h3>\
    <ul class="control presets menu">\
    {{#each items}}\
      <li><a href="#" data-preset-id="{{ @key }}">{{ name }}</a></li>\
    {{/each}}\
    </ul>\
  ');

    var PresetListView = Backbone.View.extend({
        events: {
            'click a': 'onPresetClick'
        },
        render: function() {
            var rawHTML = _template({
                items: presets
            });
            this.$el.html(rawHTML);
            this.$items = this.$el.find('a');
            return this;
        },
        onPresetClick: function(e) {
            var id = $(e.currentTarget).attr('data-preset-id');
            this.$items.removeClass('active');
            $(e.currentTarget).addClass('active');
            dispatcher.trigger(dispatcher.EventKeys.PRESET_SELECTED, presets[id]);
        }
    });

    function init(options) {
        dispatcher.register(evs);
        new PresetListView(options).render();
    }

    return {
        init: init
    }

})();





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
        Sequencer.init({
            el: $('#r-mid')
        });
        Transport.init({
            el: $('#r-top')
        });
        Metronome.init({
            el: $('#r-head')
        });
        PresetList.init({
            el: $('#r-footer')
        });
        this._connectModules();

        var pattern = {
            sequence: {
                 'kick': '1010000000110000',
                 'snare': '0000100101001001',
                 'hihat': '0000000000000000',
                 'crash': '0000000000000000',
                 'ride': '1010101010101010',
                 'rim': '0000000000000000',
                 'tom': '0000000000000000',
            }

        };

        dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_SET_PATTERN, pattern);
    },

    init: function(randomBank) {

        document.addEventListener('visibilitychange', function(e) {
            if (document.hidden) dispatcher.trigger(dispatcher.EventKeys.SEQUENCER_STOP);
        }, false);

        var samples = randomBank;

        // Load samples and kickoff
        SampleBank.init(samples, this.onLoad.bind(this));
    }
}
        $.get( "http://localhost:5000/random", function( data ) {
            console.log('initializing app with followin data: ',data)
            App.init(data)
        });