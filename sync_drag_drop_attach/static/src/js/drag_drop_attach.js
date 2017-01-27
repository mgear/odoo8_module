openerp.sync_drag_drop_attach = function (instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    
	instance.web.FormView.include({
    	check_actual_mode: function(source, options) {
        	var self = this;
			this._super.apply(this, arguments);
        	if(this.get("actual_mode") === "view") {
        	    self.$el.find('div.oe_form_sheet_width, div.oe_form_nosheet').on('dragover',function(e) {
        	        e.preventDefault();e.stopPropagation();
        	        self.$el.find('.oe_form').addClass('adjust_sheet');
        	        self.$el.find('div.hidden_formview_drop').addClass('hidden_drop_formview_highlight');
        	    })
        	    .on('dragleave', function(e){self.toggle_effect(e)})
        	    .on('drop',function(e) {
        	        if(e.originalEvent.dataTransfer && e.originalEvent.dataTransfer.files.length){
        	            self.toggle_effect(e);
        	            self.upload_files(e.originalEvent.dataTransfer.files);
        	        }
        	    });
        	} else {
        	    self.$el.find('div.oe_form_sheet_width, div.oe_form_nosheet').off('dragover').off('dragleave').off('drop');
        	}
    	},
		toggle_effect: function(e){
    	    var self = this;
    	    e.preventDefault();e.stopPropagation();
    	    self.$el.find('div.hidden_formview_drop').removeClass('hidden_drop_formview_highlight');
    	    self.$el.find('.oe_form').removeClass('adjust_sheet');
    	},
    	upload_files: function(files){
        	var self = this;
        	var total_attachements = 0;
        	_.each(files, function(file){
            	var querydata = new FormData();
            	querydata.append('callback', 'oe_fileupload_temp2');
            	querydata.append('ufile',file);
            	querydata.append('model', self.dataset.model);
            	querydata.append('id', self.datarecord.id);
            	querydata.append('multi', 'true');
            	$.ajax({
                	url: '/web/binary/upload_attachment',
                	type: 'POST',
                	data: querydata,
                	cache: false,
                	processData: false,  
                	contentType: false,
                	success: function(id){
                        self.load_record(self.datarecord);      	
            	    }
           		});
                
        	});
    	}
	});
    instance.web.Sidebar.include({
        on_attachment_changed: function(e) {
            var $e = $(e.target);
            if ($e.val() !== '') {
                this.getParent().upload_files(e.target.files);
            }
        }
    });
}