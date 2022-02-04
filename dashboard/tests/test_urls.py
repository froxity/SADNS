from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import *

"""
Unit Test for Dashboard App URL
"""

class DashboardTestURL(SimpleTestCase):
  """Dashboard"""
  def test_dashboard_url_is_resolved(self):
    url = reverse('dashboard')
    self.assertEquals(resolve(url).func, dashboard)
  
  def test_printpdf_url_is_resolved(self):
    url = reverse('dashboard_report')
    self.assertEquals(resolve(url).func.view_class, ViewPDF)

  """Webfilter"""
  def test_webfilter_url_is_resolved(self):
    url = reverse('webfilter')
    self.assertEquals(resolve(url).func, webfilter)
  
  def test_setfilter_true_is_resolved(self):
    url = reverse('setfiltertrue', args=['ex-uuid'])
    self.assertEquals(resolve(url).func, setfilter_true)
  
  def test_setfilter_false_is_resolved(self):
    url = reverse('setfilterfalse', args=['ex-uuid'])
    self.assertEquals(resolve(url).func, setfilter_false)
  
  """Domains"""
  def test_domains_url_is_resolved(self):
    url = reverse('domains')
    self.assertEquals(resolve(url).func, domains)
  
  def test_edit_wdomain_is_resolved(self):
    url = reverse('edit_wdomain', args=['ex-uuid'])
    self.assertEquals(resolve(url).func, edit_wdomain)
  
  def test_edit_bdomain_is_resolved(self):
    url = reverse('edit_bdomain', args=['ex-uuid'])
    self.assertEquals(resolve(url).func, edit_bdomain)
  
  def test_delete_wdomain_is_resolved(self):
    url = reverse('delete_wdomain', args=['ex-uuid'])
    self.assertEquals(resolve(url).func, delete_wdomain)
  
  def test_delete_bdomain_is_resolved(self):
    url = reverse('delete_bdomain', args=['ex-uuid'])
    self.assertEquals(resolve(url).func, delete_bdomain)