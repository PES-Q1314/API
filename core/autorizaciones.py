from tastypie.authorization import Authorization, ReadOnlyAuthorization


class AutorizacionDeAutor(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.autor.usuario == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.autor.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.autor.usuario == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.autor.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.autor.usuario == bundle.request.user


class AutorizacionDePerfil(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.usuario == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.usuario == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.usuario == bundle.request.user