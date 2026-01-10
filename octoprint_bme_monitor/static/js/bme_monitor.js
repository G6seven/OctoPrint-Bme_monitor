/*
 * View model for OctoPrint-Bme_monitor
 *
 * Author: G6seven
 * License: AGPL-3.0-or-later
 */
$(function() {
    function Bme_monitorViewModel(parameters) {
        var self = this;

        // Inicializace observablů pro UI
        self.bme1 = { temp: ko.observable("--"), hum: ko.observable("--"), pres: ko.observable("--") };
        self.bme2 = { temp: ko.observable("--"), hum: ko.observable("--"), pres: ko.observable("--") };

        // Příjem dat z backendu
        self.onDataUpdaterPluginMessage = function(plugin, data)
        {
            if (plugin !== "bme_monitor") return; // Název složky vašeho pluginu
            console.log("Data přijata:", data);
            if (data.bme1) {
                self.bme1.temp(data.bme1.temp);
                self.bme1.hum(data.bme1.hum);
                self.bme1.pres(data.bme1.pres);
            }
            if (data.bme2) {
                self.bme2.temp(data.bme2.temp);
                self.bme2.hum(data.bme2.hum);
                self.bme2.pres(data.bme2.pres);
            }
        };


        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/main/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: Bme_monitorViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_bme_monitor, #tab_plugin_bme_monitor, ...
        elements: [ "#tab_plugin_bme_monitor" ]
    });
});

