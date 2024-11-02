from django_tables2 import SingleTableView




def format_phone(phone_number):
    if not phone_number:
        return ""
    stripped_phone = phone_number.strip().replace(" ","").replace(".","").replace("-","")
    if len(stripped_phone)==10 and stripped_phone.isdigit():
        return "%s%s %s%s %s%s %s%s %s%s" % tuple(stripped_phone)
    elif len(stripped_phone)==13 and stripped_phone.startswith("+212"):
        return "+212 %s %s%s %s%s %s%s %s%s" % tuple(stripped_phone[4:])
    elif len(stripped_phone)==14 and stripped_phone.startswith("00212"):
        return "00212 %s %s%s %s%s %s%s %s%s" % tuple(stripped_phone[5:])
    else:
        return phone_number.strip()


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        if self.filter_class:
            self.filter = self.filter_class(self.request.GET, queryset=qs)
            if self.formhelper_class:
                self.filter.form.helper = self.formhelper_class()
            qs = self.filter.qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data(**kwargs)

        # Assurez-vous que le filtre est défini si la classe de filtre est présente
        if self.filter_class:
            if not hasattr(self, 'filter'):
                # Si self.filter n'est pas encore défini, on l'initialise
                self.get_queryset()
            context[self.context_filter_name] = self.filter
        return context

    def get_filter_kwargs(self):
        return {self.request}

    def get(self, request, *args, **kwargs):
        if hasattr(request, 'htmx') and request.htmx:
            self.template_name = "base/includes/list_table.html"
        return super().get(request, *args, **kwargs)



