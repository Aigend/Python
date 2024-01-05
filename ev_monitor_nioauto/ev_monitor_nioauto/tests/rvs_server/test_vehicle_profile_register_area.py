import pytest

class TestVehProfileRegArea(object):
    @pytest.mark.skip("Manual")
    def test_vehicle_profile_register_area(self):
        """
        修复vehicle profile和vehicle profile info extend之间，上牌地信息不一致的问题

        1、UDS推送预设主用车人到kafka: swc-uds-relation-dev-vehicle-user-relations
        工具：http://armstrong.nioint.com/#/zeus/vehicle-owner
        填写完毕，点击submit
        rvs_server消费后将数据存到history_owner_change、relation_order_account

        2、Vinbom调用 vinbom/batch_save接口：http://showdoc.nevint.com/index.php?s=/11&page_id=4688
        将订单信息推送到kafka: swc-cvs-tsp-dev-80001-vb_sync_insert/update
        rvs_server消费后将vid和订单号存到history_vinbom_change、relation_order_vehicle

        3、数据在一个relation表中存下来后，rvs_server会到另外一个relation表中通过订单号car_order_id去找数据，绑定人车关系，更新relation_user_vehicle

        # 以上为rvs更新静态信息的逻辑，与同步注册地信息的测试无直接影响，同步注册地信息逻辑实际为第四步：
        4、通过car_order_id，调用 /vom/order/select/detail 接口，从VOM拿到注册地信息，
        更新vehicle_profile/vehicle_profile_info_extend表的register_city/register_province/register_area_code

        case:
            vin: SQETEST0833037360
            vid: b011c7392c794d98bb38de09d7009079
            car_order_id: 810001585633149128
        """

