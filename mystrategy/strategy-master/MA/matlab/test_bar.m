clear;
% ��ע���޸ĳ�����ע�����û���������
username = 'demo@myquant.cn';
pwd = '123456';

global bar_5;
global bar_20;
global MA5;
global MA20;

% ��ע����������strategy_id��Ҫ���ĳ��������ն����ɵ�ID���������ն��Ͽ��������Ե�����״̬���µ���
ret = gm.Init(username,pwd,MDMode.MD_MODE_SIMULATED,'SZSE.000001.bar.60','110ca5d6-a8a1-11e5-a82d-bc855616490f','localhost:8001');

if ret ~= 0
    disp('��ʼ��ʧ��!');
    disp(ret);
    return;
end

gm.SetBarHandle(@OnBar);
gm.SetLoginHandle(@OnLogin);
gm.SetErrorHandle(@OnError);
gm.SetOrderHandle(@OnOrder);

gm.Run();