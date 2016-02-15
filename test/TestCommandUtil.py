from util.CommandUtil import CommandUtil


def test_push():
    cu = CommandUtil()
    expect_result = '75UBBKN@@KWG'
    result = cu.devices()
    # print result
    assert expect_result == result

test_push()
