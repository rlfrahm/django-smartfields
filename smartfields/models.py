

class SmartfieldsModelMixin(object):

    def __init__(self, *args, **kwargs):
        self.smartfields_handle('pre_init')
        super(SmartfieldsModelMixin, self).__init__(*args, **kwargs)
        self.smartfields_handle('post_init')


    def save(self, *args, **kwargs):
        self.smartfields_handle('pre_save')
        super(SmartfieldsModelMixin, self).save(*args, **kwargs)
        self.smartfields_handle('post_save')

    save.alters_data = True


    def delete(self, *args, **kwargs):
        self.smartfields_handle('pre_delete')
        #for manager in self.smartfields_managers:
        #    delete_handle = getattr(manager.field, 'delete', None)
        #    if callable(delete_handle):
        #        delete_handle(self)
        super(SmartfieldsModelMixin, self).delete(*args, **kwargs)
        self.smartfields_handle('post_delete')

    delete.alters_data = True                    


    def _smartfields_get_managers(self):
        if hasattr(self, 'smartfields_order'):
            managers = []
            for field_name in self.smartfields_order:
                managers.append(self._smartfields_managers[field_name])
            for field_name, manager in self._smartfields_managers.items():
                if field_name not in self.smartfields_order:
                    managers.append(manager)
        else:
            managers = self._smartfields_managers.values()
        return managers


    def smartfields_handle(self, event):
        for manager in self._smartfields_get_managers():
            manager.handle(self, event)


    def smartfields_process(self, field_names=None):
        if field_names is not None:
            field_names = set(field_names)
        for manager in self._smartfields_get_managers():
            if not field_names or manager.field.name in field_names:
                manager.process(self)


    def smartfield_status(self, field_name):
        """A way to find out a status a filed."""
        field = self._meta.get_field(field_name)
        if hasattr(field, 'get_status'):
            return field.get_status(self)
