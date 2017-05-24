<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Basic Page Needs
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <meta charset="utf-8">
    <title>Peptide Concentration Calculator</title>
    <meta name="description" content="">
    <meta name="author" content="Branko Žitko">

    <!-- Mobile Specific Metas
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- FONT
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">

    <!-- CSS
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <link rel="stylesheet" href="/css/normalize.css">
    <link rel="stylesheet" href="/css/skeleton.css">
    <link rel="stylesheet" href="/css/custom.css">
    <link rel="stylesheet" href="/css/modal.css">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="/js/modal.js"></script>


<script type="text/javascript">
    var $SCRIPT_ROOT = "{{ request.script_name }}";
    $(function() {

        var submit_form = function(e) {
            $.getJSON($SCRIPT_ROOT + '_calc', {
                peptide_seq: $('textarea[name="peptide_seq"]').val(),
                cterm: $('select[name="cterm"]').val(),
                num_ss_bonds: $('select[name="num_ss_bonds"]').val(),
                max_ss_bonds: $('select[name="num_ss_bonds"] option').length - 1,

                mw: $('[name="mw"]').val(),
                weight: $('[name="weight"]').val(),
                volume: $('[name="volume"]').val(),
                counterion: $('[name="counterion"]').val(),

                <% for model_id in sorted(models): %>
                m{{model_id}}_absorption: $('[name="m{{model_id}}_absorption"]').val(),
                m{{model_id}}_pathlength: $('[name="m{{model_id}}_pathlength"]').val(),
                m{{model_id}}_dilution: $('[name="m{{model_id}}_dilution"]').val(),                    
                <% end %>


                }, function(data) {
                    $.each(data.htmls, function(key, value ) {
                        $('[name="' + key + '"]').html(value);
                    });

                    $.each(data.values, function(key, value) {
                       $('[name="' + key + '"]').val(value); 
                    });

                    $('span').text('');

                    $.each(data.errors, function(key, value) {
                        $('#' + key).text(value);                        
                    });



                    
            });
      return false;
    };


    $(document).on('change', 'input,select,textarea', function(e) {
        submit_form(e);
    });
    //$('input').on("focusout", function(){alert(123);});

    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });

    
  });
</script>
</head>


<body>

        <div id="modal_mw" class="modal">
        <div class="modal-inner">
        <div class="modal-content">
            <div class="modal-close-icon">
            <a href="javascript:void(0)" class="close-modal"><i class="fa fa-times" aria-hidden="true"></i></a>
            </div>
            <div class="modal-content-inner">
                <h4>Peptide molecular weight</h4>
                <p>Peptide molecular weight was calculated based on the average molecular weight of each amino acid obtained from <a href="http://www.matrixscience.com/help/aa_help.html" target="blank">Mascot software homepage</a>.</p>  
            </div>
            <hr class="modal-buttons-seperator">
            <div class="modal-buttons">
                <button class="button button-primary close-modal">OK</button>
            </div>
        </div>
        </div>
        </div>


        <% for model_id in sorted(models): %>
        <div id="modal_{{model_id}}" class="modal">
        <div class="modal-inner">
        <div class="modal-content">
            <div class="modal-close-icon">
            <a href="javascript:void(0)" class="close-modal"><i class="fa fa-times" aria-hidden="true"></i></a>
            </div>
            <div class="modal-content-inner">
                {{ !infos[model_id] }}  
            </div>
            <hr class="modal-buttons-seperator">
            <div class="modal-buttons">
                <button class="button button-primary close-modal">OK</button>
            </div>
        </div>
        </div>
        </div>
        <% end %>


    <div class="container">
        <div class="row">
            <h1>Peptide Concentration Calculator</h1>
        </div>
    
        <div class="docs-section" style="background: #c0c0c0">
        <h5></h5>
        <form>
  <!-- Peptide sequence
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
            <div class="row">
                <div class="two columns">
                    <label for="peptide_seq">Peptide sequence</label>
                </div>
                <div class="six columns">
                    <textarea name="peptide_seq" type="text" class="u-full-width"></textarea>

                </div>
                <div class="four columns">
                    <span id="peptide_seq"></span>
                </div>
            </div>

  <!-- C-terrminus
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

            <div class="row">
                <div class="two columns">
                    <label for="cterm">C-terminus type</label>
                </div>
                <div class="four columns">
                <select name="cterm" class="u-full-width">
                <% for value, text in Constants.CTERMS.items(): %>
                    <option value="{{value}}">{{text}}</option>
                <% end %>
                </select>
                </div>
            </div>
            
  <!-- Number of SS bridges
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

            <div class="row">
                <div class="two columns">
                    <label for="num_ss_bonds">SS-bridges</label>
                </div>
                <div class="six columns">
                    <select name="num_ss_bonds">
                        <option value="0">0</option>
                    </select>
                </div>
                <div class="four columns">
                    <span></span>
                </div>
            </div>

        </form>
        </div>




  <!-- Extinctions
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
        <% for model_id in sorted(models): %>
        <div class="docs-section" style="background: {{models[model_id].color}};">
            <div class="row">
                <div class="three columns">
                    <label for="m{{model_id}}_extinction">Extinction coefficient at {{ model_id }} nm</label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_extinction" type="text" readonly="readonly" class="u-full-width" />
                </div>
                <div class="one columns">cm<sup>-1</sup></div>
                <div class="two columns"><button class="button-primary open-modal" data="modal_{{model_id}}">info</button></div>
            </div>

        </div>
        <% end %>

  <!-- Concetration by Weight
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->


        <div class="docs-section" style="background: #c0c0c0">
            <h5>Peptide concentration - estimate by weight</h5>

           



            <div class="row">
                <div class="two columns">
                    <label for="mw">MW</label>
                </div>
                <div class="four columns">
                    <input name="mw" readonly="readonly" type="text" class="u-full-width" />
                </div>
                <div class="one columns">Da</div>
                <div class="two columns">
                    <button class="button-primary open-modal" data="modal_mw">info</button>
                    <span id="mw"></span>
                </div>
            </div>

            <div class="row">
                <div class="two columns">
                    <label for="weight">weight</label>
                </div>
                <div class="four columns">
                    <input name="weight" type="text" class="u-full-width" />
                </div>
                <div class="one columns">mg</div>
                <div class="two columns"><span id="weight"></span></div>
            </div>

            <div class="row">
                <div class="two columns">
                    <label for="volume">volume</label>
                </div>
                <div class="four columns">
                    <input name="volume" type="text" class="u-full-width" />
                </div>
                <div class="one columns">ml</div>
                <div class="two columns"><span id="volume"></span></div>
            </div>

            <div class="row">
                <div class="two columns">
                    <label for="volume">counterion</label>
                </div>
                <div class="four columns">
                    <select name="counterion">
                        <% for counterion in Model.COUNTERIONS: %>
                            <option value="{{counterion}}">{{counterion}}</option>
                        <% end %>
                    </select>
                </div>
            </div>

            <div class="row">
                <div class="two columns">
                    <label for="mw_ci">MW with C.I. (for K, R and N-t)</label>
                </div>
                <div class="four columns">
                    <input name="mw_ci" readonly="readonly" type="text" class="u-full-width" />
                </div>
                <div class="one columns">Da</div>
                <div class="two columns"></div>
            </div>

            <div class="row">
                <div class="two columns">
                    <label for="peptide1">Peptide concentration</label>
                </div>
                <div class="four columns">
                    <input name="peptide1" readonly="readonly" type="text" class="u-full-width" />
                </div>
                <div class="one columns">mg/ml</div>
                <div class="two columns"></div>
            </div>

            <div class="row">
                <div class="two columns">
                    <label for="peptide2"></label>
                </div>
                <div class="four columns">
                    <input name="peptide2" readonly="readonly" type="text" class="u-full-width" />
                </div>
                <div class="one columns">mM</div>
                <div class="two columns"></div>
            </div>

            
            <% for model_id in sorted(models): %>
            <div class="row">
                <div class="two columns">
                    <label for="m{{model_id}}_expected">expected A<sub>{{model_id}}</sub></label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_expected" readonly="readonly" type="text" class="u-full-width" />
                </div>
                <div class="one columns"></div>
                <div class="two columns"></div>
            </div>
            <% end %>


        </div>


  <!-- Concetration by extinction
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

        <% for model_id in sorted(models): %>
        <div class="docs-section" style="background: {{models[model_id].color}}">
            <h6></h6>
            <div class="row">
                <div class="four columns">
                    <label for="m{{model_id}}_absorption">measured absorption at {{model_id}}nm A</label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_absorption" type="text" class="u-full-width" />
                </div>
                <div class="one columns"></div>
                <div class="two columns"><span id="m{{model_id}}_absorption"></span></div>
            </div>

            <div class="row">
                <div class="four columns">
                    <label for="m{{model_id}}_extinction">extinction coefficient (ε<sub>{{model_id}}</sub>)</label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_extinction" readonly="readonly" type="text" class="u-full-width" />
                </div>
                <div class="two columns">M<sup>-1</sup>cm<sup>-1</sup></div>
                <div class="two columns"><span id="m{{model_id}}_extinction"></div>
            </div>

            <div class="row">
                <div class="four columns">
                    <label for="m{{model_id}}_pathlength">pathlength (l)</label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_pathlength" type="text" class="u-full-width" />
                </div>
                <div class="one columns">cm</div>
                <div class="two columns"><span id="m{{model_id}}_pathlength"></span></div>
            </div>

            <div class="row">
                <div class="four columns">
                    <label for="m{{model_id}}_dilution">dilution factor</label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_dilution" type="text" class="u-full-width" />
                </div>
                <div class="one columns">fold</div>
                <div class="two columns"><span id="m{{model_id}}_dilution"></span></div>
            </div>

            <div class="row">
                <div class="four columns">
                    <label for="m{{model_id}}_c">estimated concentration (from A<sub>{{model_id}}</sub>)</label>
                </div>
                <div class="four columns">
                    <input name="m{{model_id}}_c" type="text" readonly="readonly" class="u-full-width" />
                </div>
                <div class="one columns">mM</div>
                <div class="two columns"></div>
            </div>



        </div>
        <% end %>


    </div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
</html>
