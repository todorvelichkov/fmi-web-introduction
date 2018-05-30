# Django basics

## apps, urls, views and templates
* use `settings.py` to add new apps

```
    INSTALLED_APPS = [
        # ...
        'calc',
    ]
```

Now code some functionality

* `calc/views.py`
    ```
        # -*- coding: utf-8 -*-
        from __future__ import unicode_literals

        from django.shortcuts import render

        from django.http import HttpResponse, HttpResponseRedirect


        # Create your views here.
        def calc(request):

            if request.method == 'POST':
                filters = request.POST.copy()

                x = int(filters.get('x', 0))
                y = int(filters.get('y', 0))
                operation = {
                    'add': lambda x,y: x+y,
                    'substract': lambda x, y: x-y,
                }.get(filters.get('operation', 'add'))

                result = operation(x,y)

                filters['result'] = result

                return HttpResponseRedirect(request.path+'?'+filters.urlencode())

            filters = request.GET.copy()
            filters.setdefault('x', '0')
            filters.setdefault('y', '0')
            filters.setdefault('operation', 'add')

            return render(request, 'calc/templates/calc_index.html', {
                'filters': filters,
        })
    ```

* `calc/templates/calc_index.html`
    ```
        <form method="POST">
            {% csrf_token %}
            <input type="text" name="x" value="{{filters.x}}">
            <select name='operation'>
                <option 
                    value="add" 
                    {% if filters.operation == 'add' %}
                        selected="selected"
                    {%endif %}
                >+</option>  
                <option value="substract"
                    {% if filters.operation == 'substract' %}
                        selected="selected"
                    {%endif %}
                >-</option>    
            </select>
            <input type="text" name="y" value="{{filters.y}}">
            <input type="submit" name="calc" value="calc">
        </form>


            POST: {{request.POST}}
            <hr/>
            FILTERS: {{filters}}


        <hr/>

        {% if filters.result %}
            RESULT: {{filters.result}}
        {% endif %}
    ```

* `calc/urls.py`
    ```
        from django.conf.urls import url

        from calc.views import calc

        urlpatterns = [
            url(r'^$', calc),
        ]
    ```

* `simple_project/urls.py` includes the `calc.urls`
    ```
        urlpatterns = [
            # ...
            url(r'^calc/', include('calc.urls')),
            # ...
        ]
    ```

## How do we abstract all this? Forms and models!

* `calc/forms.py`
    ```
        from django import forms
        from calc.models import CalcResult

        class CalcForm(forms.ModelForm):
            # x = forms.IntegerField(label='x value')
            # operation = forms.ChoiceField(choices=[
            #     ('add', 'Add'),
            #     ('substract', 'Substract'),
            # ])
            # y = forms.IntegerField(label='y value')

            class Meta:
                model = CalcResult
        fields = ['x', 'operation', 'y']
    ```

* `calc/models.py`
    ```

        # -*- coding: utf-8 -*-
        from __future__ import unicode_literals

        from django.db import models
        from django.http import QueryDict
        from django.urls import reverse
        from django.core.exceptions import ValidationError

        class CalcResult(models.Model):
            x = models.IntegerField()
            y = models.IntegerField()
            operation = models.CharField(
                max_length=20,
                choices=[
                ('add', 'Add'),
                ('substract', 'Substract'),
            ])
            result = models.FloatField()

            def get_absolute_url(self):
                q = QueryDict(mutable=True)
                pub_attrs = {k:v for k,v in self.__dict__.items() if not k.startswith('_')}
                q.update(pub_attrs)
                return  '%s?%s' % (
                    reverse('calc_index'),
                    q.urlencode()
                )

            def clean(self):
                self.result = self.get_result()
                # if not self.result == self.get_result():
                #     raise ValidationError({'result': 'InvalidResult'})

            def get_result(self):
                operation = {
                    'add': lambda x,y: x+y,
                    'substract': lambda x, y: x-y,
                }.get(self.operation)

                return operation(self.x, self.y)

            def __str__(self):
                return '<Res: %s>' % (
                    self.result,
        )
    ```

* `calc/urls.py`
    ```
        
        from django.conf.urls import url

        from calc.views import calc

        urlpatterns = [
            url(r'^index/$', calc, name='calc_index'),
        ]
    ```

* `calc/views.py`
    ```

        # -*- coding: utf-8 -*-
        from __future__ import unicode_literals

        from django.shortcuts import render

        from django.http import HttpResponse, HttpResponseRedirect
        from calc.forms import CalcForm
        from calc.models import CalcResult

        # Create your views here.
        def calc(request):
            if request.method == 'POST':
                form = CalcForm(request.POST)

                if form.is_valid():
                    calc_res = form.save()

                    return HttpResponseRedirect(
                        calc_res.get_absolute_url()
                    )
            else:
                filters = request.GET.copy()
                filters.setdefault('x', '0')
                filters.setdefault('y', '0')
                filters.setdefault('operation', 'add')
                form = CalcForm(filters)

            results = CalcResult.objects.all()
            return render(request, 'calc/calc_index.html', {
                'form': form,
                'results': results,
        })
    ```

* `calc/calc_index.html`
    ```
        <form method="POST">
            {% csrf_token %}
            {{form}}
            <input type="submit" name="calc" value="calc">
        </form>

        {% if request.GET.result %}
            RESULT: {{request.GET.result}}
        {% endif %}

        <table>
            <tr>
                <th>x</th>
                <th>operation</th>
                <th>y</th>
                <th>result</th>
                <th>view</th>
            </tr>
            {% for result in results %}
                <tr>
                    <td>{{result.x}}</td>
                    <td>{{result.operation}}</td>
                    <td>{{result.y}}</td>
                    <td>{{result.result}}</td>
                    <td>
                        <a href="{{result.get_absolute_url}}">
                            view
                        </a>
                    </td>
                </tr>
            {% endfor %}
        </table>
    ```